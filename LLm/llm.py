from transformers import AutoModelForCausalLM, AutoTokenizer
from gtts import gTTS
import os

class TinyLlamaWrapper:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        print("Chargement du tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("Chargement du modèle...")
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print("Modèle prêt !")

    def generate_response(self, prompt, max_new_tokens=200, temperature=0.7):
        messages = [
            {"role": "system", "content": "Tu es MIKO-AI, un assistant utile. Réponds toujours en français. Sois poli."},
            {"role": "user", "content": prompt}
        ]

        formatted = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
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

        # TTS avec gTTS
        tts = gTTS(text=response, lang="fr")
        tts.save("response.mp3")
        os.system("start response.mp3")  # Joue le fichier sur Windows

        return response

if __name__ == "__main__":
    llm = TinyLlamaWrapper()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = llm.generate_response(user_input)
        print("\033[96mMIKO-AI :\033[0m", response)