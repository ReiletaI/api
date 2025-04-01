import torch
import os
import subprocess
from pyannote.audio import Pipeline

class DiarizationService:
    def __init__(self, huggingface_token):
        self.huggingface_token = huggingface_token
        self._pipeline = None
        
    def _load_pipeline(self):
        """Lazy loading of the diarization pipeline to save memory"""
        if self._pipeline is None:
            try:
                self._pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=self.huggingface_token
                )
                
                # Use GPU if available
                if torch.cuda.is_available():
                    self._pipeline.to(torch.device("cuda"))
                    print("Diarization pipeline loaded on GPU")
                else:
                    self._pipeline.to(torch.device("cpu"))
                    print("Diarization pipeline loaded on CPU")
                    
            except Exception as e:
                print(f"Error loading diarization pipeline: {e}")
                raise
        
        return self._pipeline
    
    def format_time(self, seconds):
        """Converts seconds to MM:SS format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def perform_diarization(self, audio_path):
        """
        Perform speaker diarization on audio file
        
        Args:
            audio_path: Path to the audio file to analyze
            
        Returns:
            List of tuples (turn, speaker) where turn is a Segment object with start/end times
        """
        try:
            # Get pipeline
            pipeline = self._load_pipeline()
            
            # Clear GPU memory if using CUDA
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Perform diarization
            diarization = pipeline(audio_path)
            
            # Post-process results
            diarization_result = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                if turn.end - turn.start > 1.0:  # Ignore segments that are too short
                    diarization_result.append((turn, speaker))
                    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            
            return diarization_result
            
        except Exception as e:
            print(f"Diarization error: {e}")
            return []