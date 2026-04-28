# It's tts too btw.
from transformers import AutoModelForCausalLM, AutoTokenizer

class TinyLlamaWrapper:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print("Model ready!")

    def generate_response(self, prompt, max_new_tokens=200, temperature=0.7):
        messages = [
            {"role": "system", "content": "Tu es MIKO-AI, un assistant utile. Réponds toujours en français. Sois poli."},
            {"role": "user", "content": prompt}
        ]
        formatted = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(formatted, return_tensors="pt", truncation=True)
        input_length = inputs["input_ids"].shape[1]
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
        )
        new_tokens = outputs[0][input_length:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()