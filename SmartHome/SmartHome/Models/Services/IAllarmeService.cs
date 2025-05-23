using SmartHome.Models.Entities;

namespace SmartHome.Services
{
    public interface IAllarmeService
    {
        Task<IEnumerable<Allarme>> GetAllarmiAsync();
        Task<Allarme?> GetAllarmeByIdAsync(int id);
        Task<IEnumerable<Allarme>> GetAllarmiBySensoreAsync(int sensoreId);
        Task<Allarme> CreaAllarmeAsync(int sensoreId, string messaggio);
        Task<bool> RisolviAllarmeAsync(int id);
    }
}