let port;
let reader;
let writer;
let keepReading = true;
let dotNetHelper = null;
let isConnected = false;

export function connectSerial(dotNetRef) {
    dotNetHelper = dotNetRef;

    navigator.serial.requestPort().then(selectedPort => {
        port = selectedPort;
        return port.open({ baudRate: 9600 });
    }).then(() => {
        isConnected = true;
        console.log("Connessione seriale stabilita");

        // Setup per la lettura
        const decoder = new TextDecoderStream();
        const inputDone = port.readable.pipeTo(decoder.writable);
        reader = decoder.readable.getReader();

        // Setup per la scrittura
        const encoder = new TextEncoderStream();
        const outputDone = encoder.readable.pipeTo(port.writable);
        writer = encoder.writable.getWriter();

        // Notifica la connessione riuscita
        dotNetHelper.invokeMethodAsync("OnConnessioneStabilita", true);

        readLoop();
    }).catch(err => {
        console.error("Errore connessione seriale:", err);
        isConnected = false;
        dotNetHelper?.invokeMethodAsync("OnConnessioneStabilita", false);
    });
}

async function readLoop() {
    while (port?.readable && keepReading && isConnected) {
        try {
            const { value, done } = await reader.read();
            if (done) break;

            if (value && value.trim()) {
                console.log("DATO RICEVUTO:", value.trim());
                dotNetHelper?.invokeMethodAsync("RiceviDatoSeriale", value.trim());
            }
        } catch (err) {
            console.error("Errore lettura seriale:", err);
            if (err.name === 'NetworkError') {
                // La connessione è stata persa
                isConnected = false;
                dotNetHelper?.invokeMethodAsync("OnConnessionePersa");
            }
            break;
        }
    }
}

export async function sendData(data) {
    if (!isConnected || !writer) {
        console.error("Non connesso alla porta seriale");
        return false;
    }

    try {
        await writer.write(data + '\n'); // Aggiunge newline per terminare il comando
        console.log("DATO INVIATO:", data);
        return true;
    } catch (err) {
        console.error("Errore invio dati:", err);
        if (err.name === 'NetworkError') {
            isConnected = false;
            dotNetHelper?.invokeMethodAsync("OnConnessionePersa");
        }
        return false;
    }
}

export async function disconnectSerial() {
    console.log("Disconnessione in corso...");

    keepReading = false;

    try {
        // Chiudi reader
        if (reader) {
            await reader.cancel();
            await reader.releaseLock();
            reader = null;
        }

        // Chiudi writer
        if (writer) {
            await writer.close();
            writer = null;
        }

        // Chiudi porta
        if (port) {
            await port.close();
            port = null;
        }

        isConnected = false;
        console.log("Disconnessione completata");
        dotNetHelper?.invokeMethodAsync("OnDisconnessione");

    } catch (err) {
        console.error("Errore durante la disconnessione:", err);
    }
}

export function getConnectionStatus() {
    return isConnected;
}

export function cleanup() {
    dotNetHelper = null;
}