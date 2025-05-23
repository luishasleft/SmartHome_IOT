using System.ComponentModel.DataAnnotations;

namespace SmartHome.Models.Entities;

public class Sensore
{
    [Key]
    public int Id { get; set; }
        
    [Required]
    [MaxLength(100)]
    public string Nome { get; set; } = string.Empty;
        
    [Required]
    [MaxLength(50)]
    public string Tipo { get; set; } = string.Empty; // 'Temperatura', 'Movimento', 'LuceRGB', etc.
        

        
    public string? Valore { get; set; } // Ultimo valore letto
        
    public DateTime DataLettura { get; set; }
        
    public bool Attivo { get; set; } = true;
        
    // Navigation property
    public virtual ICollection<Evento> Eventi { get; set; } = new List<Evento>();
    public virtual ICollection<Allarme> Allarmi { get; set; } = new List<Allarme>();
}