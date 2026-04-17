from generator import WatermarkedGenerator
from detector import detect_watermark
from utils import text_to_tokens

generator = WatermarkedGenerator(secret_key="yash123")

prompt = "Artificial intelligence is"

print("\n--- Generating Watermarked Text ---\n")
generated_text = generator.generate(prompt)
print(generated_text)

print("\n--- Detecting Watermark ---\n")
tokens = text_to_tokens(generated_text)

result = detect_watermark(tokens, "yash123", generator.vocab_size)

print(f"Green Ratio: {result['green_ratio']:.4f}")
print(f"Z-Score:     {result['z_score']:.4f}")
print(f"Watermarked: {result['is_watermarked']}")