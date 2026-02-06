namespace Desision.Services.MarketScanner;

public sealed class MarketScannerOptions
{
    public const string SectionName = "MarketScanner";

    public int IntervalSeconds { get; set; } = 60;
    public int TopSymbolsCount { get; set; } = 15;
    public bool UseTestNet { get; set; } = false;
}
