using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SmartHome.Models.Entities;

public class Allarme
{
    [Key]
    public int Id { get; set; }
        
    [Required]
    public int SensoreId { get; set; }
        
    [Required]
    [MaxLength(500)]
    public string Messaggio { get; set; } = string.Empty;
        
    public DateTime DataCreazione { get; set; }
        
    public bool Risolto { get; set; } = false;
        
    // Navigation property
    [ForeignKey(nameof(SensoreId))]
    public virtual Sensore Sensore { get; set; } = null!;
}