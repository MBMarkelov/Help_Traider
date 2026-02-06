using System.Collections.Concurrent;
using System.Globalization;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Options;

namespace Desision.Services.MarketScanner;

public sealed class BybitWebSocketMarketDataStream : IBybitMarketDataStream
{
    private readonly ILogger<BybitWebSocketMarketDataStream> _logger;
    private readonly MarketScannerOptions _options;
    private readonly ConcurrentDictionary<string, decimal> _volumeBySymbol = new(StringComparer.OrdinalIgnoreCase);

    public BybitWebSocketMarketDataStream(
        IOptions<MarketScannerOptions> options,
        ILogger<BybitWebSocketMarketDataStream> logger)
    {
        _options = options.Value;
        _logger = logger;
    }

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Starting Bybit WebSocket stream: {Url}", _options.WebSocketUrl);

        using var socket = new ClientWebSocket();
        await socket.ConnectAsync(new Uri(_options.WebSocketUrl), cancellationToken);

        await SubscribeAsync(socket, cancellationToken);
        await ReceiveLoopAsync(socket, cancellationToken);
    }

    public IReadOnlyCollection<MarketSymbolVolume> GetTopByVolume(int count)
    {
        var snapshot = _volumeBySymbol
            .OrderByDescending(pair => pair.Value)
            .Take(count)
            .Select(pair => new MarketSymbolVolume(pair.Key, pair.Value))
            .ToArray();

        return snapshot;
    }

    private async Task SubscribeAsync(ClientWebSocket socket, CancellationToken cancellationToken)
    {
        var payload = new
        {
            op = "subscribe",
            args = _options.Topics,
        };

        var json = JsonSerializer.Serialize(payload);
        var bytes = Encoding.UTF8.GetBytes(json);
        await socket.SendAsync(bytes, WebSocketMessageType.Text, true, cancellationToken);
    }

    private async Task ReceiveLoopAsync(ClientWebSocket socket, CancellationToken cancellationToken)
    {
        var buffer = new byte[64 * 1024];

        while (!cancellationToken.IsCancellationRequested && socket.State == WebSocketState.Open)
        {
            var result = await socket.ReceiveAsync(buffer, cancellationToken);
            if (result.MessageType == WebSocketMessageType.Close)
            {
                _logger.LogWarning("Bybit WebSocket closed by server.");
                break;
            }

            var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
            TryProcessMessage(message);
        }
    }

    private void TryProcessMessage(string message)
    {
        try
        {
            using var document = JsonDocument.Parse(message);
            if (!document.RootElement.TryGetProperty("data", out var dataElement))
            {
                return;
            }

            if (dataElement.ValueKind == JsonValueKind.Array)
            {
                foreach (var entry in dataElement.EnumerateArray())
                {
                    TryUpdateVolume(entry);
                }

                return;
            }

            if (dataElement.ValueKind == JsonValueKind.Object)
            {
                TryUpdateVolume(dataElement);
            }
        }
        catch (JsonException jsonException)
        {
            _logger.LogDebug(jsonException, "Skipped non-JSON message from Bybit WebSocket.");
        }
    }

    private void TryUpdateVolume(JsonElement entry)
    {
        if (!entry.TryGetProperty("s", out var symbolElement))
        {
            return;
        }

        var symbol = symbolElement.GetString();
        if (string.IsNullOrWhiteSpace(symbol))
        {
            return;
        }

        if (!TryReadDecimal(entry, "v", out var volume) &&
            !TryReadDecimal(entry, "vol24h", out volume))
        {
            return;
        }

        _volumeBySymbol[symbol] = volume;
    }

    private static bool TryReadDecimal(JsonElement entry, string propertyName, out decimal value)
    {
        value = 0m;
        if (!entry.TryGetProperty(propertyName, out var property))
        {
            return false;
        }

        if (property.ValueKind == JsonValueKind.Number && property.TryGetDecimal(out value))
        {
            return true;
        }

        if (property.ValueKind == JsonValueKind.String)
        {
            return decimal.TryParse(property.GetString(), NumberStyles.Any, CultureInfo.InvariantCulture, out value);
        }

        return false;
    }
}
