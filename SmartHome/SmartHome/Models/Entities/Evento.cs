using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SmartHome.Models.Entities;

public class Evento
{
    [Key]
    public int Id { get; set; }
        
    [Required]
    public int SensoreId { get; set; }
        
    [Required]
    public string Valore { get; set; } = string.Empty;
        
    public DateTime Timestamp { get; set; }
    // Navigation property
    [ForeignKey(nameof(SensoreId))]
    public virtual Sensore Sensore { get; set; } = null!;
}
