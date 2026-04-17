import React, { useState } from "react";
import Generate from "./components/Generate";
import Detect from "./components/Detect";
import "./styles.css";

function App() {
  const [generatedText, setGeneratedText] = useState("");
  const [detectText, setDetectText] = useState("");
  const [toastVisible, setToastVisible] = useState(false);

  const handleCopyToDetect = () => {
    if (generatedText) {
      setDetectText(generatedText);
      setToastVisible(true);
      setTimeout(() => setToastVisible(false), 2000);
    }
  };

  return (
    <div className="container">
      <div className="app-header">
        <h1>LLMGuard 🛡️</h1>
        <p className="tagline">AI-Generated Text Watermarking & Detection</p>
      </div>

      <Generate
        onTextGenerated={setGeneratedText}
        onCopyToDetect={handleCopyToDetect}
        hasOutput={!!generatedText}
      />

      <Detect
        text={detectText}
        onTextChange={setDetectText}
      />

      <div className="app-footer">
        <p>Built with GPT-2 • Watermark Algorithm by LLMGuard</p>
      </div>

      <div className={`copy-toast ${toastVisible ? "show" : ""}`}>
        ✅ Copied to Detect section!
      </div>
    </div>
  );
}

export default App;