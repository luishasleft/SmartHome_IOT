using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace SmartHome.Migrations
{
    /// <inheritdoc />
    public partial class Init : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Sensori",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Nome = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    Tipo = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    Valore = table.Column<string>(type: "TEXT", nullable: true),
                    DataLettura = table.Column<DateTime>(type: "TEXT", nullable: false, defaultValueSql: "CURRENT_TIMESTAMP"),
                    Attivo = table.Column<bool>(type: "INTEGER", nullable: false, defaultValue: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Sensori", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Allarmi",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    SensoreId = table.Column<int>(type: "INTEGER", nullable: false),
                    Messaggio = table.Column<string>(type: "TEXT", maxLength: 500, nullable: false),
                    DataCreazione = table.Column<DateTime>(type: "TEXT", nullable: false, defaultValueSql: "CURRENT_TIMESTAMP"),
                    Risolto = table.Column<bool>(type: "INTEGER", nullable: false, defaultValue: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Allarmi", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Allarmi_Sensori_SensoreId",
                        column: x => x.SensoreId,
                        principalTable: "Sensori",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Eventi",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    SensoreId = table.Column<int>(type: "INTEGER", nullable: false),
                    Valore = table.Column<string>(type: "TEXT", nullable: false),
                    Timestamp = table.Column<DateTime>(type: "TEXT", nullable: false, defaultValueSql: "CURRENT_TIMESTAMP")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Eventi", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Eventi_Sensori_SensoreId",
                        column: x => x.SensoreId,
                        principalTable: "Sensori",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.InsertData(
                table: "Sensori",
                columns: new[] { "Id", "Attivo", "Nome", "Tipo", "Valore" },
                values: new object[,]
                {
                    { 1, true, "Temperatura Salotto", "Temperatura", null },
                    { 2, true, "Movimento Ingresso", "Movimento", null },
                    { 3, true, "Luce RGB Camera", "LuceRGB", null },
                    { 4, true, "Ventola Cucina", "Ventola", null },
                    { 5, true, "Buzzer Sistema", "Buzzer", null },
                    { 6, true, "Badge Principale", "Badge", null }
                });

            migrationBuilder.CreateIndex(
                name: "IX_Allarmi_SensoreId",
                table: "Allarmi",
                column: "SensoreId");

            migrationBuilder.CreateIndex(
                name: "IX_Eventi_SensoreId",
                table: "Eventi",
                column: "SensoreId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Allarmi");

            migrationBuilder.DropTable(
                name: "Eventi");

            migrationBuilder.DropTable(
                name: "Sensori");
        }
    }
}
