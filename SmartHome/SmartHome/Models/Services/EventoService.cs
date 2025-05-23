using Microsoft.EntityFrameworkCore;
using SmartHome.Data;
using SmartHome.Models.Entities;

public class EventoService : IEventoService
{
    private readonly HomeDbContext _context;

    public EventoService(HomeDbContext context)
    {
        _context = context;
    }

    public async Task<List<Evento>> GetAllAsync() =>
        await _context.Eventi
            .Include(e => e.Sensore)
            .OrderByDescending(e => e.Timestamp)
            .ToListAsync();

    public async Task<List<Evento>> GetBySensoreAsync(int sensoreId) =>
        await _context.Eventi
            .Where(e => e.SensoreId == sensoreId)
            .OrderByDescending(e => e.Timestamp)
            .ToListAsync();

    public async Task AddAsync(Evento evento)
    {
        _context.Eventi.Add(evento);
        await _context.SaveChangesAsync();
    }
}