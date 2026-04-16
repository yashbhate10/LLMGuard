from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import numpy as np
from watermark import get_green_tokens, apply_watermark

class WatermarkedGenerator:
    def __init__(self, secret_key="secret123"):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.secret_key = secret_key

        self.vocab_size = self.model.config.vocab_size
        self.green_tokens = get_green_tokens(self.vocab_size, secret_key)

    def generate(self, prompt, max_length=50):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")

        for _ in range(max_length):
            outputs = self.model(input_ids)
            logits = outputs.logits[0, -1].detach().numpy()

            # Apply watermark
            logits = apply_watermark(logits, self.green_tokens)

            probs = torch.softmax(torch.tensor(logits), dim=0).numpy()
            next_token = np.random.choice(len(probs), p=probs)

            input_ids = torch.cat(
                [input_ids, torch.tensor([[next_token]])], dim=1
            )

        return self.tokenizer.decode(input_ids[0])