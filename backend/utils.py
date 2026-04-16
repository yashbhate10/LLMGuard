from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def text_to_tokens(text):
    return tokenizer.encode(text)