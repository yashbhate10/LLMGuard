import React, { useState } from "react";
import axios from "axios";

function Generate({ onTextGenerated, onCopyToDetect, hasOutput }) {
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateText = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError("");
    setOutput("");

    try {
      const res = await axios.post("http://localhost:5000/generate", {
        prompt: prompt,
      });
      const text = res.data.generated_text;
      setOutput(text);
      onTextGenerated(text);
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>
        <span className="icon">✨</span>
        Generate Watermarked Text
      </h2>

      <textarea
        placeholder="Enter a prompt, e.g. 'Artificial intelligence is...'"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        disabled={loading}
      />

      <div className="btn-row">
        <button
          className="btn-primary"
          onClick={generateText}
          disabled={loading || !prompt.trim()}
        >
          {loading ? (
            <>
              <span className="spinner"></span> Generating...
            </>
          ) : (
            "Generate"
          )}
        </button>

        {hasOutput && (
          <button className="btn-secondary" onClick={onCopyToDetect}>
            📋 Copy to Detect
          </button>
        )}
      </div>

      {error && (
        <div className="output" style={{ borderColor: "rgba(239,68,68,0.4)" }}>
          <p style={{ color: "#fca5a5" }}>⚠️ {error}</p>
        </div>
      )}

      {output && (
        <div className="output">
          <h3>Generated Output</h3>
          <p className="generated-text">{output}</p>
        </div>
      )}
    </div>
  );
}

export default Generate;