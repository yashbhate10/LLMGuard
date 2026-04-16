import React, { useState } from "react";
import axios from "axios";

function Generate() {
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState("");

  const generateText = async () => {
    const res = await axios.post("http://localhost:5000/generate", {
      prompt: prompt,
    });
    setOutput(res.data.generated_text);
  };

  return (
    <div className="card">
      <h2>Generate Watermarked Text</h2>
      <textarea
        placeholder="Enter prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={generateText}>Generate</button>

      {output && (
        <div className="output">
          <h3>Output:</h3>
          <p>{output}</p>
        </div>
      )}
    </div>
  );
}

export default Generate;