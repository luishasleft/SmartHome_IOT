using Microsoft.EntityFrameworkCore;
using SmartHome.Data;
using SmartHome.Models.Entities;

public class SensoreService : ISensoreService
{
    private readonly HomeDbContext _context;

    public SensoreService(HomeDbContext context)
    {
        _context = context;
    }

    public async Task<List<Sensore>> GetAllAsync() =>
        await _context.Sensori.ToListAsync();

    public async Task<Sensore?> GetByIdAsync(int id) =>
        await _context.Sensori.FindAsync(id);

    public async Task AddAsync(Sensore sensore)
    {
        _context.Sensori.Add(sensore);
        await _context.SaveChangesAsync();
    }
}