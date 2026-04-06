from voice import transcribe_audio  # À ajouter dans voice.py (voir plus bas)
from LLM import TinyLlamaWrapper

def main():
    llm = TinyLlamaWrapper()

    while True:
        # 1. Enregistrement et transcription
        user_text = transcribe_audio()
        print(f"\033[92mToi :\033[0m {user_text}")

        # 2. Génération de la réponse
        if user_text.lower() in ["quit", "exit", "bye"]:
            break

        response = llm.generate_response(user_text)
        print(f"\033[96mMIKO-AI :\033[0m {response}")

if __name__ == "__main__":
    main()