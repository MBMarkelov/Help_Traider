var builder = DistributedApplication.CreateBuilder(args);

builder.AddProject<Projects.Desision>("desision");

builder.Build().Run();
