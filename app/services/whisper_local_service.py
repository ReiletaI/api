import whisper

class WhisperLocalService:
    def __init__(self, model_name : str):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path : str):
        result = self.model.transcribe(audio_path, task="translate")
        return result["text"]
        