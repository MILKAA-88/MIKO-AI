import requests

def chat(message, historique=[]):
    historique.append({"role": "user", "content": message})
    
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": "local-model",
            "messages": [
                {"role": "system", "content": "Tu es MIKO AI, un assistant intelligent. Tu est là, pour répondre et aider l'utilisateur, sois précis, gentil avec un ton d'humour. Si tu ne sais pas quoi répondre notifie-le à l'utilisateur."}
            ] + historique
        }
    )
    
    reponse_texte = response.json()["choices"][0]["message"]["content"]
    historique.append({"role": "assistant", "content": reponse_texte})
    
    return reponse_texte

# Boucle de conversation
print("MIKO AI — tape 'quitter' pour arrêter\n")
historique = []

while True:
    user_input = input("Toi : ")
    if user_input.lower() == "quitter":
        break
    
    reponse = chat(user_input, historique)
    print(f"MIKO : {reponse}\n")