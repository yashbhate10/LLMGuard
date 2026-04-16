import numpy as np

def detect_watermark(token_ids, secret_key, vocab_size):
    green_count = 0

    for token in token_ids:
        if hash((token, secret_key)) % 2 == 0:
            green_count += 1

    ratio = green_count / len(token_ids)

    # Expected ~0.5, watermark → higher
    z_score = (ratio - 0.5) / (0.5 / np.sqrt(len(token_ids)))

    return {
        "green_ratio": ratio,
        "z_score": z_score,
        "is_watermarked": ratio > 0.6
    }