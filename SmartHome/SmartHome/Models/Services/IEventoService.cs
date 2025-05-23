using SmartHome.Models.Entities;

public interface IEventoService
{
    Task<List<Evento>> GetAllAsync();
    Task<List<Evento>> GetBySensoreAsync(int sensoreId);
    Task AddAsync(Evento evento);
}