using SmartHome.Models.Entities;

public interface ISensoreService
{
    Task<List<Sensore>> GetAllAsync();
    Task<Sensore?> GetByIdAsync(int id);
    Task AddAsync(Sensore sensore);
}