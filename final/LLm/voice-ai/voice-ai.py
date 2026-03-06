import pyttsx3

engine = pyttsx3.init()

# Configuration de la voix
engine.setProperty('rate', 150)    # Vitesse (150 = normal)
engine.setProperty('volume', 0.5)  # Volume (0.0 à 1.0)

# Lister les voix disponibles
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"{i} : {voice.name}")

engine.setProperty('voice', voices[0].id)

engine.say("Bonjour, je suis miko hey aie ! Votre assistant virtuel gratuit et intélligent.")
engine.runAndWait()