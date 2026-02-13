from transformers import pipeline
from config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE

generator = pipeline("text-generation", model=MODEL_NAME)

def generate(prompt):
    result = generator(
        prompt,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        do_sample=True,
        pad_token_id=50256
    )
    return result[0]["generated_text"]
