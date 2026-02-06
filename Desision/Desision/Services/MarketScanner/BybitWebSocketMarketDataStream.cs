using bybit.net.api.WebSocketStream;
using Desision.Services.MarketScanner;
using Microsoft.Extensions.Options;
using System.Collections.Concurrent;
using System.Globalization;
using System.Text.Json;

public sealed class BybitWebSocketMarketDataStream : IBybitMarketDataStream
{
    private readonly ILogger<BybitWebSocketMarketDataStream> _logger;
    private readonly MarketScannerOptions _options;

    private readonly ConcurrentDictionary<string, decimal> _volumeBySymbol =
        new(StringComparer.OrdinalIgnoreCase);

    private BybitSpotWebSocket? _webSocket;

    public BybitWebSocketMarketDataStream(
        IOptions<MarketScannerOptions> options,
        ILogger<BybitWebSocketMarketDataStream> logger)
    {
        _options = options.Value;
        _logger = logger;
    }

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Starting Bybit Spot WebSocket market scanner");

        _webSocket = new BybitSpotWebSocket(
            useTestNet: _options.UseTestNet,
            pingIntevral: 5);

        _webSocket.OnMessageReceived(
            async data =>
            {
                TryProcessTicker(data);
                await Task.CompletedTask;
            },
            cancellationToken);

        await _webSocket.ConnectAsync(
            new[] { "tickers.BTCUSDT" },
            cancellationToken);
    }

    public IReadOnlyCollection<MarketSymbolVolume> GetTopByVolume(int count)
    {
        return _volumeBySymbol
            .OrderByDescending(x => x.Value)
            .Take(count)
            .Select(x => new MarketSymbolVolume(x.Key, x.Value))
            .ToArray();
    }

    private void TryProcessTicker(string rawMessage)
    {
        try
        {
            _logger.LogInformation("RAW WS MESSAGE: {Message}", rawMessage);

            using var doc = JsonDocument.Parse(rawMessage);

            if (!doc.RootElement.TryGetProperty("data", out var data))
                return;

            if (data.ValueKind == JsonValueKind.Array)
            {
                foreach (var ticker in data.EnumerateArray())
                {
                    UpdateVolume(ticker);
                }
            }
            else if (data.ValueKind == JsonValueKind.Object)
            {
                UpdateVolume(data);
            }
        }
        catch (Exception ex)
        {
            _logger.LogDebug(ex, "Failed to parse ticker message");
        }
    }

    private void UpdateVolume(JsonElement ticker)
    {
        if (!ticker.TryGetProperty("symbol", out var symbolElement))
            return;

        var symbol = symbolElement.GetString();
        if (string.IsNullOrWhiteSpace(symbol))
            return;

        if (!TryReadDecimal(ticker, "turnover24h", out var volume))
            return;

        _volumeBySymbol[symbol] = volume;
    }

    private static bool TryReadDecimal(JsonElement element, string property, out decimal value)
    {
        value = 0m;

        if (!element.TryGetProperty(property, out var prop))
            return false;

        return prop.ValueKind switch
        {
            JsonValueKind.Number => prop.TryGetDecimal(out value),
            JsonValueKind.String => decimal.TryParse(
                prop.GetString(),
                NumberStyles.Any,
                CultureInfo.InvariantCulture,
                out value),
            _ => false
        };
    }
}
