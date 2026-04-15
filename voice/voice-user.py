import whisper

model = whisper.load_model("small")

result = model.transcribe(
    "sd-st-song.mp3",
    language="fr",
    fp16=False,
    verbose=True,
    word_timestamps=True
)

print(result["text"])

# It's just a test.