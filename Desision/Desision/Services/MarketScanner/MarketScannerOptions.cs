namespace Desision.Services.MarketScanner;

public sealed class MarketScannerOptions
{
    public const string SectionName = "MarketScanner";

    public int IntervalSeconds { get; set; } = 60;
    public int TopSymbolsCount { get; set; } = 15;
    public string WebSocketUrl { get; set; } = "wss://stream.bybit.com/v5/public/spot";
    public string[] Topics { get; set; } = ["tickers"];
}
