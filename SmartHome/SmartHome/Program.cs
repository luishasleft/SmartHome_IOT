using Microsoft.EntityFrameworkCore;
using SmartHome.Components;
using SmartHome.Data;
using SmartHome.Services;

var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddDbContext<HomeDbContext>(options =>
    options.UseSqlite(connectionString));

builder.Services.AddScoped<IAllarmeService, AllarmeService>();
builder.Services.AddScoped<ISensoreService, SensoreService>();
builder.Services.AddScoped<IEventoService, EventoService>();


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();


app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();