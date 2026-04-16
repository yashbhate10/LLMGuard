import React from "react";
import Generate from "./components/Generate";
import Detect from "./components/Detect";
import "./styles.css";

function App() {
  return (
    <div className="container">
      <h1>LLMGuard 🔐</h1>
      <Generate />
      <Detect />
    </div>
  );
}

export default App;