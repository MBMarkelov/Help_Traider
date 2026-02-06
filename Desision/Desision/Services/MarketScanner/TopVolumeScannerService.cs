using Microsoft.Extensions.Options;

namespace Desision.Services.MarketScanner;

public sealed class TopVolumeScannerService : BackgroundService
{
    private readonly IBybitMarketDataStream _marketDataStream;
    private readonly ILogger<TopVolumeScannerService> _logger;
    private readonly MarketScannerOptions _options;

    public TopVolumeScannerService(
        IBybitMarketDataStream marketDataStream,
        IOptions<MarketScannerOptions> options,
        ILogger<TopVolumeScannerService> logger)
    {
        _marketDataStream = marketDataStream;
        _options = options.Value;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var streamTask = _marketDataStream.StartAsync(stoppingToken);
        using var timer = new PeriodicTimer(TimeSpan.FromSeconds(Math.Max(5, _options.IntervalSeconds)));

        while (await timer.WaitForNextTickAsync(stoppingToken))
        {
            var topSymbols = _marketDataStream.GetTopByVolume(_options.TopSymbolsCount);
            if (topSymbols.Count == 0)
            {
                _logger.LogInformation("Scanner: no volume data yet from Bybit.");
                continue;
            }

            var summary = string.Join(", ", topSymbols.Select(item => $"{item.Symbol}:{item.Volume:F2}"));
            _logger.LogInformation("Scanner snapshot (top {Count}): {Summary}", topSymbols.Count, summary);
        }

        await streamTask;
    }
}
