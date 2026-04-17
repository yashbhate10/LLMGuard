import numpy as np
import hashlib


def detect_watermark(token_ids, secret_key, vocab_size, z_threshold=3.0):
    """
    Detect whether text contains a watermark by computing a Z-Score
    on the proportion of 'green' tokens.

    Uses the same SHA-256 hashing as watermark.py to ensure the green token
    partition is identical. Classification uses a statistical Z-Score threshold
    instead of a naive ratio cutoff, providing:
    - Lower false positives on short texts.
    - Lower false negatives on long texts.

    Args:
        token_ids: list of integer token IDs from the text.
        secret_key: the secret key used during watermark generation.
        vocab_size: vocabulary size of the model.
        z_threshold: Z-Score threshold for classification (default 3.0).

    Returns:
        dict with green_ratio, z_score, and is_watermarked.
    """
    if len(token_ids) == 0:
        return {
            "green_ratio": 0.0,
            "z_score": 0.0,
            "is_watermarked": False
        }

    green_count = 0

    for token in token_ids:
        h = hashlib.sha256(f"{token}-{secret_key}".encode()).hexdigest()
        if int(h, 16) % 2 == 0:
            green_count += 1

    n = len(token_ids)
    ratio = green_count / n

    # Under null hypothesis (no watermark), green ratio ~ 0.5
    # Standard deviation = 0.5 / sqrt(n)
    z_score = float((ratio - 0.5) / (0.5 / np.sqrt(n)))

    return {
        "green_ratio": float(round(ratio, 4)),
        "z_score": float(round(z_score, 4)),
        "is_watermarked": bool(z_score > z_threshold)
    }