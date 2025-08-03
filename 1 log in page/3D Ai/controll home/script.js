let port;
let writer;

// Connect to Arduino
async function connectToArduino() {
  try {
    port = await navigator.serial.requestPort(); // Ask user to select port
    await port.open({ baudRate: 9600 });

    writer = port.writable.getWriter();
    document.getElementById("status").textContent = "✅ Connected to Arduino";
  } catch (e) {
    console.error("Connection failed", e);
    document.getElementById("status").textContent = "❌ Connection failed";
  }
}

// Send command (typed or spoken)
async function sendCommand() {
  const input = document.getElementById("command").value;
  const command = input.toLowerCase().replace(/[^\w\s]/gi, '').trim();  // Clean input

  if (!writer) {
    alert("Please connect to Arduino first.");
    return;
  }

  let signal;

  switch (command) {
    case "first light on": signal = "A"; break;
    case "first light off": signal = "B"; break;
    case "second light on": signal = "C"; break;
    case "second light off": signal = "D"; break;
    case "fan on": signal = "E"; break;
    case "fan off","fan of": signal = "F"; break;
    case "street light on": signal = "G"; break;
    case "street light off": signal = "H"; break;
    case "door open": signal = "I"; break;
    case "door close": signal = "J"; break;
    case "all lights on": signal = "K"; break;
    case "all lights off": signal = "L"; break;
    case "acharya activate" : signal = "M" ; break;
    default:
      alert("Unknown command!");
      return;
  }

  const data = new TextEncoder().encode(signal);
  await writer.write(data);
  document.getElementById("status").textContent = `✅ Sent: ${command}`;
}

// Voice recognition using Web Speech API
function startListening() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Speech Recognition is not supported in this browser.");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.start();

  recognition.onstart = () => {
    document.getElementById("status").textContent = "🎙 Listening...";
  };

  recognition.onresult = (event) => {
    const speechResult = event.results[0][0].transcript
      .toLowerCase()
      .replace(/[^\w\s]/gi, '')
      .trim();

    document.getElementById("command").value = speechResult;
    document.getElementById("status").textContent = `🎧 Heard: "${speechResult}"`;

    // ✅ Automatically run command without pressing "Send"
    sendCommand();
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error", event.error);
    document.getElementById("status").textContent = "❌ Voice recognition error";
  };

  // Optional: Keep listening again and again
  // recognition.onend = () => recognition.start(); // uncomment if you want continuous listening
}
