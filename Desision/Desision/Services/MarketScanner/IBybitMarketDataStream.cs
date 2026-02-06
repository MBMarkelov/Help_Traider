namespace Desision.Services.MarketScanner;

public interface IBybitMarketDataStream
{
    Task StartAsync(CancellationToken cancellationToken);
    IReadOnlyCollection<MarketSymbolVolume> GetTopByVolume(int count);
}
