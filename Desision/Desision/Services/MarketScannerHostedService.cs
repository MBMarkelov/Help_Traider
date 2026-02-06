using Desision.Services.MarketScanner;

namespace Desision.Services
{
    public sealed class MarketScannerHostedService : BackgroundService
    {
        private readonly IBybitMarketDataStream _stream;
        private readonly ILogger<MarketScannerHostedService> _logger;

        public MarketScannerHostedService(
            IBybitMarketDataStream stream,
            ILogger<MarketScannerHostedService> logger)
        {
            _stream = stream;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("MarketScannerHostedService started");

            await _stream.StartAsync(stoppingToken);

            while (!stoppingToken.IsCancellationRequested)
            {
                await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);

                var top = _stream.GetTopByVolume(15);
                _logger.LogInformation("Top symbols snapshot:");

                foreach (var s in top)
                {
                    _logger.LogInformation("{Symbol} -> {Volume}", s.Symbol, s.Volume);
                }
            }
        }
    }

}
