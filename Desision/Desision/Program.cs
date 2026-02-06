using Dapper;
using Desision.Services;
using Desision.Services.MarketScanner;
using Microsoft.Extensions.Options;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MarketScannerOptions>(
    builder.Configuration.GetSection(MarketScannerOptions.SectionName));

builder.Services.AddSingleton<IBybitMarketDataStream, BybitWebSocketMarketDataStream>();

builder.Services.AddLogging(cfg =>
{
    cfg.ClearProviders();
    cfg.AddConsole();
});
builder.Services.AddHostedService<MarketScannerHostedService>();

var app = builder.Build();

app.Run();
