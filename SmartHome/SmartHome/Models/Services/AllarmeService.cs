using Microsoft.EntityFrameworkCore;
using SmartHome.Data;
using SmartHome.Models.Entities;

namespace SmartHome.Services
{
    public class AllarmeService : IAllarmeService
    {
        private readonly HomeDbContext _context;

        public AllarmeService(HomeDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Allarme>> GetAllarmiAsync()
        {
            return await _context.Allarmi
                .Include(a => a.Sensore)
                .OrderByDescending(a => a.DataCreazione)
                .ToListAsync();
        }

        public async Task<Allarme?> GetAllarmeByIdAsync(int id)
        {
            return await _context.Allarmi
                .Include(a => a.Sensore)
                .FirstOrDefaultAsync(a => a.Id == id);
        }

        public async Task<IEnumerable<Allarme>> GetAllarmiBySensoreAsync(int sensoreId)
        {
            return await _context.Allarmi
                .Where(a => a.SensoreId == sensoreId)
                .OrderByDescending(a => a.DataCreazione)
                .ToListAsync();
        }

        public async Task<Allarme> CreaAllarmeAsync(int sensoreId, string messaggio)
        {
            var allarme = new Allarme
            {
                SensoreId = sensoreId,
                Messaggio = messaggio,
                DataCreazione = DateTime.Now,
                Risolto = false
            };

            _context.Allarmi.Add(allarme);
            await _context.SaveChangesAsync();

            return allarme;
        }

        public async Task<bool> RisolviAllarmeAsync(int id)
        {
            var allarme = await _context.Allarmi.FindAsync(id);
            if (allarme == null) return false;

            allarme.Risolto = true;
            await _context.SaveChangesAsync();
            return true;
        }
    }
}