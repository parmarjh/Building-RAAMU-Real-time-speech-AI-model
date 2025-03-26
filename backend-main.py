import asyncio
import logging
from typing import Dict, Any

import torch
import transformers
import sounddevice as sd
import numpy as np

from src.audio_processing.preprocessor import AudioPreprocessor
from src.speech_recognition.recognizer import SpeechRecognizer
from src.nlp.intent_processor import IntentProcessor
from src.response_generation.generator import ResponseGenerator
from src.text_to_speech.synthesizer import SpeechSynthesizer

class SpeechAISystem:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Speech AI System with configurable components
        
        Args:
            config (Dict[str, Any]): Configuration for system components
        """
        # Logging setup
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Device configuration
        self.device = self._configure_device()

        # Audio processing module
        self.audio_preprocessor = AudioPreprocessor(
            sample_rate=config.get('sample_rate', 16000),
            chunk_duration=config.get('chunk_duration', 0.1)
        )

        # Speech recognition engine
        self.speech_recognizer = SpeechRecognizer(
            model_path=config.get('asr_model', 'models/multilingual_asr'),
            device=self.device
        )

        # NLP intent processor
        self.intent_processor = IntentProcessor(
            model_path=config.get('nlp_model', 'models/intent_classifier')
        )

        # Response generation
        self.response_generator = ResponseGenerator(
            model_path=config.get('response_model', 'models/response_generator')
        )

        # Text-to-speech synthesizer
        self.speech_synthesizer = SpeechSynthesizer(
            model_path=config.get('tts_model', 'models/multilingual_tts')
        )

    def _configure_device(self) -> torch.device:
        """
        Configure optimal device for processing
        
        Returns:
            torch.device: Optimal computation device
        """
        if torch.cuda.is_available():
            self.logger.info("Using CUDA GPU for processing")
            return torch.device('cuda')
        elif torch.backends.mps.is_available():
            self.logger.info("Using MPS (Apple Silicon) for processing")
            return torch.device('mps')
        else:
            self.logger.info("Using CPU for processing")
            return torch.device('cpu')

    async def process_audio_stream(self, audio_chunk: np.ndarray) -> Dict[str, Any]:
        """
        Process a chunk of audio through the entire AI pipeline
        
        Args:
            audio_chunk (np.ndarray): Input audio chunk
        
        Returns:
            Dict[str, Any]: Processing results
        """
        try:
            # Preprocess audio
            processed_audio = self.audio_preprocessor.process(audio_chunk)

            # Perform speech recognition
            transcription = self.speech_recognizer.transcribe(processed_audio)

            # Detect language
            detected_language = self.speech_recognizer.detect_language(transcription)

            # Process intent
            intent = self.intent_processor.classify_intent(
                transcription, 
                language=detected_language
            )

            # Generate response
            response = self.response_generator.generate(
                transcription, 
                intent=intent, 
                language=detected_language
            )

            # Synthesize speech response
            audio_response = self.speech_synthesizer.synthesize(
                response, 
                language=detected_language
            )

            return {
                'transcription': transcription,
                'language': detected_language,
                'intent': intent,
                'response': response,
                'audio_response': audio_response
            }

        except Exception as e:
            self.logger.error(f"Error in audio processing pipeline: {e}")
            return {
                'error': str(e)
            }

    def start_streaming_inference(self, sample_rate: int = 16000):
        """
        Start continuous audio streaming and inference
        
        Args:
            sample_rate (int): Audio sampling rate
        """
        def audio_callback(indata, frames, time, status):
            if status:
                self.logger.warning(f"Audio stream status: {status}")
            
            # Convert to numpy array and process
            audio_chunk = indata.flatten()
            asyncio.create_task(self.process_audio_stream(audio_chunk))

        try:
            with sd.InputStream(
                samplerate=sample_rate, 
                channels=1,
                callback=audio_callback
            ):
                # Keep the stream open
                sd.sleep(float('inf'))
        except Exception as e:
            self.logger.error(f"Error in audio streaming: {e}")

def main():
    # Example configuration
    config = {
        'sample_rate': 16000,
        'chunk_duration': 0.1,
        'asr_model': 'models/multilingual_asr',
        'nlp_model': 'models/intent_classifier',
        'response_model': 'models/response_generator',
        'tts_model': 'models/multilingual_tts'
    }

    # Initialize Speech AI System
    speech_ai = SpeechAISystem(config)

    # Start streaming inference
    speech_ai.start_streaming_inference()

if __name__ == "__main__":
    main()
