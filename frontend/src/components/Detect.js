import React, { useState } from "react";
import axios from "axios";

function Detect({ text, onTextChange }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const detectText = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await axios.post("http://localhost:5000/detect", {
        text: text,
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Detection failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>
        <span className="icon">🔍</span>
        Detect Watermark
      </h2>

      <textarea
        placeholder="Paste or copy text here to check for watermarks..."
        value={text}
        onChange={(e) => onTextChange(e.target.value)}
        disabled={loading}
      />

      <div className="btn-row">
        <button
          className="btn-primary"
          onClick={detectText}
          disabled={loading || !text.trim()}
        >
          {loading ? (
            <>
              <span className="spinner"></span> Analyzing...
            </>
          ) : (
            "Detect Watermark"
          )}
        </button>
      </div>

      {error && (
        <div className="output" style={{ borderColor: "rgba(239,68,68,0.4)" }}>
          <p style={{ color: "#fca5a5" }}>⚠️ {error}</p>
        </div>
      )}

      {result && (
        <div className="output">
          <h3>Analysis Results</h3>
          <div className="result-grid">
            <div className="result-item">
              <div className="label">Green Ratio</div>
              <div className="value" style={{ color: "#818cf8" }}>
                {result.green_ratio.toFixed(4)}
              </div>
            </div>
            <div className="result-item">
              <div className="label">Z-Score</div>
              <div className="value" style={{ color: "#a78bfa" }}>
                {result.z_score.toFixed(4)}
              </div>
            </div>
            <div className="result-item">
              <div className="label">Confidence</div>
              <div className="value" style={{ color: "#38bdf8" }}>
                {result.confidence !== undefined
                  ? (result.confidence * 100).toFixed(0) + "%"
                  : "N/A"}
              </div>
            </div>
            <div
              className={`verdict ${
                result.is_watermarked ? "watermarked" : "human"
              }`}
            >
              {result.is_watermarked
                ? "⚠️ AI-Generated (Watermark Detected)"
                : "✅ Likely Human-Written"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Detect;