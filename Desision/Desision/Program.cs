using Dapper;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Строка подключения (из docker-compose)
string connectionString = "Host=localhost;Database=crypto_db;Username=admin;Password=secret1";

app.MapGet("/api/candles/{symbol}", async (string symbol, int limit = 100) =>
{
    using var connection = new NpgsqlConnection(connectionString);
    
    // Запрос последних N свечей
    var sql = @"SELECT time, symbol, open, high, low, close, volume 
                FROM candles 
                WHERE symbol = @symbol 
                ORDER BY time DESC 
                LIMIT @limit";

    var candles = await connection.QueryAsync<CandleDto>(sql, new { symbol = symbol.ToUpper(), limit });
    
    // Возвращаем данные (Python легко их распарсит)
    return Results.Ok(candles);
});

app.Run();