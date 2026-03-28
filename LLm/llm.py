from transformers import AutoModelForCausalLM, AutoTokenizer

class TinyLlamaWrapper:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        print("Chargement du tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("Chargement du modèle...")
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print("Modèle prêt !")

    def generate_response(self, prompt, max_new_tokens=200, temperature=0.7):
        # Format chat correct pour TinyLlama
        messages = [
            {"role": "system", "content": "Tu es MIKO-AI, un assistant utile. Réponds toujours en français."},
            {"role": "user", "content": prompt}
        ]

        # Applique le template du modèle
        formatted = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True  # Ajoute <|assistant|> à la fin
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
        response = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        return response

if __name__ == "__main__":
    llm = TinyLlamaWrapper()
    while True:
        user_input = input("Toi : ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = llm.generate_response(user_input)
        print("MIKO-AI :", response)