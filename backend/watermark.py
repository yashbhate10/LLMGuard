import numpy as np

def get_green_tokens(vocab_size, secret_key):
    green_tokens = set()
    for i in range(vocab_size):
        if hash((i, secret_key)) % 2 == 0:
            green_tokens.add(i)
    return green_tokens


def apply_watermark(logits, green_tokens, strength=1.5):
    # Increase probability of green tokens
    for token_id in green_tokens:
        logits[token_id] *= strength
    return logits