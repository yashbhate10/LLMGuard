import React, { useState } from "react";
import axios from "axios";

function Detect() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const detectText = async () => {
    const res = await axios.post("http://localhost:5000/detect", {
      text: text,
    });
    setResult(res.data);
  };

  return (
    <div className="card">
      <h2>Detect Watermark</h2>
      <textarea
        placeholder="Paste text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={detectText}>Detect</button>

      {result && (
        <div className="output">
          <p><b>Green Ratio:</b> {result.green_ratio.toFixed(2)}</p>
          <p><b>Z-Score:</b> {result.z_score.toFixed(2)}</p>
          <p>
            <b>Result:</b>{" "}
            {result.is_watermarked ? "⚠️ AI Generated" : "✅ Human-like"}
          </p>
        </div>
      )}
    </div>
  );
}

export default Detect;