import whisper


def recognize(filename: str) -> str:
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    #audio = whisper.pad_or_trim(whisper.load_audio("output.wav"))
    return result["text"]
    #return whisper.transcribe(model, audio, task="translate", fp16=False)["text"]result["text"]
