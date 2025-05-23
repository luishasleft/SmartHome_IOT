using Microsoft.EntityFrameworkCore;
using SmartHome.Models.Entities;

namespace SmartHome.Data
{
    public class HomeDbContext : DbContext
    {
        public DbSet<Sensore> Sensori { get; set; }
        public DbSet<Evento> Eventi { get; set; }
        public DbSet<Allarme> Allarmi { get; set; }

        public HomeDbContext(DbContextOptions<HomeDbContext> options) : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configurazione Sensore
            modelBuilder.Entity<Sensore>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Nome).IsRequired().HasMaxLength(100);
                entity.Property(e => e.Tipo).IsRequired().HasMaxLength(50);

                entity.Property(e => e.DataLettura).HasDefaultValueSql("CURRENT_TIMESTAMP");
                entity.Property(e => e.Attivo).HasDefaultValue(true);
            });

            // Configurazione Evento
            modelBuilder.Entity<Evento>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Valore).IsRequired();
                entity.Property(e => e.Timestamp).HasDefaultValueSql("CURRENT_TIMESTAMP");
                
                entity.HasOne(e => e.Sensore)
                      .WithMany(s => s.Eventi)
                      .HasForeignKey(e => e.SensoreId)
                      .OnDelete(DeleteBehavior.Cascade);
            });



            // Configurazione Allarme
            modelBuilder.Entity<Allarme>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Messaggio).IsRequired().HasMaxLength(500);
                entity.Property(e => e.DataCreazione).HasDefaultValueSql("CURRENT_TIMESTAMP");
                entity.Property(e => e.Risolto).HasDefaultValue(false);
                
                entity.HasOne(a => a.Sensore)
                      .WithMany(s => s.Allarmi)
                      .HasForeignKey(a => a.SensoreId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Dati iniziali
            SeedData(modelBuilder);
        }

        private void SeedData(ModelBuilder modelBuilder)
        {
            // Sensori iniziali
            modelBuilder.Entity<Sensore>().HasData(
                new Sensore { Id = 1, Nome = "Temperatura Salotto", Tipo = "Temperatura" },
                new Sensore { Id = 2, Nome = "Movimento Ingresso", Tipo = "Movimento" },
                new Sensore { Id = 3, Nome = "Luce RGB Camera", Tipo = "LuceRGB" },
                new Sensore { Id = 4, Nome = "Ventola Cucina", Tipo = "Ventola" },
                new Sensore { Id = 5, Nome = "Buzzer Sistema", Tipo = "Buzzer" },
                new Sensore { Id = 6, Nome = "Badge Principale", Tipo = "Badge" }
            );


        }
    }
}