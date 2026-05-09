from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class LLM:
    def __init__(self):
        print("Loading LLM (Groq)...")
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.historique = [
            {
                "role": "system",
                "content": (
                    "You are MIKO, an AI assistant. "
                    "You are curious and helpful personality. "
                    "Your responses are converted to audio via TTS, so: "
                    "always respond in French, be concise (2-3 sentences max), "
                    "avoid symbols, lists and markdown, "
                    "speak naturally as in a real conversation."
                )
            }
        ]
        print("Model ready!")

    def generate_response(self, prompt, **kwargs):
        self.historique.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.historique,
            max_tokens=150
        )
        reponse_texte = response.choices[0].message.content.strip()
        self.historique.append({"role": "assistant", "content": reponse_texte})
        return reponse_texte