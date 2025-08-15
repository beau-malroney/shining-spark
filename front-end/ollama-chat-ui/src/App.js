import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [ttsEnabled, setTtsEnabled] = useState(() => {
    return localStorage.getItem("ttsEnabled") === "true";
  });
  const [voiceURI, setVoiceURI] = useState(localStorage.getItem("voiceURI") || "");
  const [rate, setRate] = useState(parseFloat(localStorage.getItem("rate")) || 1);
  const [pitch, setPitch] = useState(parseFloat(localStorage.getItem("pitch")) || 1);
  const [messages, setMessages] = useState([]);
  const [prompt, setPrompt] = useState("");
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages]);

  useEffect(() => {
    localStorage.setItem("ttsEnabled", ttsEnabled);
  }, [ttsEnabled]);

  useEffect(() => {
    localStorage.setItem("voiceURI", voiceURI);
  }, [voiceURI]);

  useEffect(() => {
    localStorage.setItem("rate", rate);
  }, [rate]);

  useEffect(() => {
    localStorage.setItem("pitch", pitch);
  }, [pitch]);

  const [voices, setVoices] = useState([]);

  useEffect(() => {
    const loadVoices = () => {
      const synthVoices = window.speechSynthesis.getVoices();
      setVoices(synthVoices);
    };

    window.speechSynthesis.onvoiceschanged = loadVoices;
    loadVoices();
  }, []);

  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    setMessages(prev => [...prev, { role: "user", content: prompt }]);

    try {
      const formData = new FormData();
      formData.append("prompt", prompt);

      const res = await axios.post("http://localhost:8000/chat", formData);
      const response = res.data.response;

      setMessages(prev => [...prev, { role: "assistant", content: response }]);
      if (ttsEnabled) {
        speak(response);
      }

    } catch (err) {
      setMessages(prev => [...prev, { role: "error", content: err.message }]);
    }

    setPrompt("");
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = rate;
    utterance.pitch = pitch;

    const selectedVoice = voices.find(v => v.voiceURI === voiceURI);
    if (selectedVoice) utterance.voice = selectedVoice;

    speechSynthesis.speak(utterance);
  };

  const previewVoice = () => {
    const utterance = new SpeechSynthesisUtterance("This is your current voice preview.");
    utterance.rate = rate;
    utterance.pitch = pitch;

    const selectedVoice = voices.find(v => v.voiceURI === voiceURI);
    if (selectedVoice) utterance.voice = selectedVoice;

    speechSynthesis.cancel(); // Stop any ongoing speech
    speechSynthesis.speak(utterance);
  };


  const startVoiceInput = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.onresult = (event) => {
      setPrompt(event.results[0][0].transcript);
    };
    recognition.start();
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;

    for (let file of files) {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://localhost:8000/upload", formData);
      setMessages(prev => [...prev, { role: "file", content: `📎 ${res.data.filename} uploaded` }]);
    }
  };

  return (
    <div className="container">
      <h1>Ollama Chat</h1>
      <div className="chat" ref={chatRef}>
        {messages.map((msg, i) => (
          <div key={i} className={`msg ${msg.role}`}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <div className="toggle">
        <label>
          <input
            type="checkbox"
            checked={ttsEnabled}
            onChange={() => setTtsEnabled(!ttsEnabled)}
          />
          🔊 Enable Text-to-Speech
        </label>
      </div>
      <div className="settings">
        <label>
          Voice:
          <select value={voiceURI} onChange={(e) => setVoiceURI(e.target.value)}>
            {voices.map((v, i) => (
              <option key={i} value={v.voiceURI}>
                {v.name} ({v.lang})
              </option>
            ))}
          </select>
        </label>

        <label>
          Rate: {rate.toFixed(1)}
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={rate}
            onChange={(e) => setRate(parseFloat(e.target.value))}
          />
        </label>

        <label>
          Pitch: {pitch.toFixed(1)}
          <input
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={pitch}
            onChange={(e) => setPitch(parseFloat(e.target.value))}
          />
        </label>
      </div>
      <button onClick={previewVoice}>🔊 Preview Voice</button>

      <div className="input-section">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your prompt..."
        />
        <button onClick={startVoiceInput}>🎙️ Speak</button>
        <button onClick={sendPrompt}>Send</button>
      </div>

      <div
        className="dropzone"
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        📁 Drag & Drop Files or Photos Here
      </div>
    </div>
  );
}

export default App;
