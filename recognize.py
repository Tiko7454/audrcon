import whisper


def recognize(filename: str) -> str:
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]
