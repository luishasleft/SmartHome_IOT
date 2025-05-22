# 🏠 Smart Home Web App con Blazor + micro:bit + Database

Questo progetto è una Web App sviluppata in **Blazor** che si connette a un **micro:bit** via USB per ricevere dati dai sensori e salvarli in un **database** per storico e controllo domotico.  
L’obiettivo è creare un sistema smart home semplice ma estendibile, con gestione di eventi, sensori, allarmi e utenti.

---

## 🔧 Fase 1 – Setup Ambiente Base

- [ ] Crea il progetto Blazor (WebAssembly o Server)
- [ ] Configura il database (SQL Server / SQLite / PostgreSQL)
- [ ] Aggiungi e configura **Entity Framework Core**
- [ ] Crea i modelli dati: `Sensore`, `EventoSensore`, `Utente`, ecc.

---

## 🗂️ Fase 2 – Progetta e Crea lo Schema DB

- [ ] Definisci le entità e le loro relazioni
- [ ] Implementa il `DbContext`
- [ ] Esegui migrazione iniziale (`dotnet ef migrations add Init`)
- [ ] Crea fisicamente il DB (`dotnet ef database update`)

---

## ⚙️ Fase 3 – Servizi lato server

- [ ] Crea i servizi C# (`SensoreService`, `EventoService`, ecc.)
- [ ] Implementa i metodi per:
  - Inserimento eventi
  - Recupero storico dati
- [ ] Se usi Blazor WebAssembly:
  - Crea Web API (REST) o SignalR per comunicare col server

---

## 🔌 Fase 4 – Connessione micro:bit via Web Serial API

- [ ] Crea uno script JS (`serial.js`) per leggere via `navigator.serial`
- [ ] Gestisci apertura porta, lettura byte e decodifica
- [ ] Passa i dati letti a Blazor via `DotNetObjectReference`

---

## 📲 Fase 5 – Integrazione in Blazor

- [ ] Crea un componente Blazor per:
  - Connettere al micro:bit
  - Mostrare i dati in tempo reale
- [ ] Alla ricezione dati:
  - Aggiorna UI (`StateHasChanged`)
  - Salva i dati nel DB tramite servizio C#

---

## 📊 Fase 6 – Dashboard e storico

- [ ] Crea pagine per:
  - Lista eventi/sensori
  - Filtri temporali
  - Dettagli evento
- [ ] Aggiungi grafici (es. con [Chart.js](https://www.chartjs.org/) o [Radzen.Blazor](https://blazor.radzen.com/chart))

---

## 🧠 Fase 7 – Funzionalità Avanzate

- [ ] Notifiche automatiche (email, alert, suoni)
- [ ] Gestione utenti, login, ruoli
- [ ] Badge e accesso controllato
- [ ] Integrazione con moduli WiFi / Bluetooth (opzionale)

---

## 🚀 Fase 8 – Testing e Deploy

- [ ] Testa con micro:bit reale collegato via USB
- [ ] Verifica salvataggio corretto nel database
- [ ] Ottimizza UI/UX
- [ ] Deploy su:
  - Azure App Service
  - VPS
  - Raspberry Pi (se vuoi farlo super nerd 😎)

---

## 📎 Requisiti

- .NET 7/8 SDK
- Visual Studio o VS Code
- micro:bit v1 o v2
- Browser compatibile con Web Serial API (Chrome o Edge)

---

## 🧠 Funzionalità del sistema Smart Home

- 🔒 **Sistema di allarme**: rilevamento movimenti con sensore PIR, attivazione allarme visivo/sonoro e registrazione evento.
- 💡 **Controllo luci**: gestione dell'accensione/spegnimento luci tramite micro:bit o da interfaccia web.
- 🧾 **Storico eventi**: salvataggio dati nel database per visualizzare eventi passati, tipo di evento, timestamp e sensore coinvolto.
- 🔐 **Accesso tramite badge**: autenticazione tramite badge RFID/NFC simulato dal micro:bit, con eventi di accesso memorizzati.
- 🧭 **Interfaccia web**: dashboard Blazor per visualizzare dati in tempo reale, storico, e controllare i dispositivi.
- 🔄 **Integrazione con micro:bit via USB**: ricezione diretta dei dati dal micro:bit attraverso Web Serial API.

