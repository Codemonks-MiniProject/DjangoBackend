import whisper

model = whisper.load_model("base")  # You can change to "small", "medium", or "large"

def transcribe_audio(audio_path):
    try:
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print("Whisper error:", e)
        return ""
    

def analyze_technical_content(transcript):
    keywords = [
        "database", "algorithm", "complexity", "inheritance", "encapsulation",
        "API", "network", "virtualization", "operating system", "compiler",
        "data structure", "machine learning", "artificial intelligence", "recursion"
    ]

    found = sum(1 for word in keywords if word.lower() in transcript.lower())
    total = len(keywords)

    score = round((found / total) * 100, 2)
    return score