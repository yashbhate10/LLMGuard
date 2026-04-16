from flask import Flask, request, jsonify
from generator import WatermarkedGenerator
from detector import detect_watermark
from utils import text_to_tokens
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Initialize model once (efficient)
generator = WatermarkedGenerator(secret_key="yash123")


# ✅ Health check route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "LLMGuard API running",
        "model": "GPT-2 Watermarked",
        "version": "1.0"
    })


# ✅ Generate endpoint
@app.route("/generate", methods=["POST"])
def generate():
    start_time = time.time()
    data = request.get_json()

    # 🔴 Validation
    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data["prompt"]
    max_length = data.get("max_length", 50)

    if len(prompt.strip()) == 0:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    if max_length > 200:
        return jsonify({"error": "max_length too large (max 200)"}), 400

    try:
        print(f"[INFO] Generating text for prompt: {prompt}")

        text = generator.generate(prompt, max_length=max_length)

        response_time = round(time.time() - start_time, 2)

        return jsonify({
            "generated_text": text,
            "meta": {
                "max_length": max_length,
                "response_time_sec": response_time
            }
        })

    except Exception as e:
        print(f"[ERROR] Generation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Detect endpoint
@app.route("/detect", methods=["POST"])
def detect():
    start_time = time.time()
    data = request.get_json()

    # 🔴 Validation
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]

    if len(text.strip()) == 0:
        return jsonify({"error": "Text cannot be empty"}), 400

    try:
        print(f"[INFO] Detecting watermark...")

        tokens = text_to_tokens(text)
        result = detect_watermark(tokens, "yash123", generator.vocab_size)

        # ✅ Add confidence score
        z_score = result["z_score"]
        confidence = min(abs(z_score) / 5, 1.0)  # normalize

        response_time = round(time.time() - start_time, 2)

        return jsonify({
            "green_ratio": result["green_ratio"],
            "z_score": z_score,
            "confidence": round(confidence, 2),
            "is_watermarked": result["is_watermarked"],
            "meta": {
                "tokens_analyzed": len(tokens),
                "response_time_sec": response_time
            }
        })

    except Exception as e:
        print(f"[ERROR] Detection failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)