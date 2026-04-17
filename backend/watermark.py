import numpy as np
import hashlib


def get_green_tokens(vocab_size, secret_key):
    """
    Deterministically partition the vocabulary into 'green' and 'red' tokens
    using SHA-256 hashing. This ensures the green list is identical across
    server restarts and different Python processes.
    """
    green_tokens = set()
    for i in range(vocab_size):
        h = hashlib.sha256(f"{i}-{secret_key}".encode()).hexdigest()
        if int(h, 16) % 2 == 0:
            green_tokens.add(i)
    return green_tokens


def apply_watermark(logits, green_tokens, delta=2.5):
    """
    Apply watermark by ADDING a constant bias (delta) to green token logits.

    Using additive bias instead of multiplicative ensures:
    - Tokens with negative logits are correctly boosted (not suppressed).
    - The watermark strength is uniform across all green tokens.

    Args:
        logits: numpy array of raw logit scores from the model.
        green_tokens: set of token IDs classified as 'green'.
        delta: additive bias strength (default 2.5).

    Returns:
        Modified logits array with watermark applied.
    """
    for token_id in green_tokens:
        logits[token_id] += delta
    return logits