import React, { useState, useEffect, useCallback } from 'react';
import { Mic, StopCircle } from 'lucide-react';

// WebSocket for real-time communication
interface SpeechProcessingResult {
  transcription: string;
  language: string;
  intent: string;
  response: string;
  audioResponse?: string;
}

const SpeechAIInterface: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [response, setResponse] = useState('');
  const [language, setLanguage] = useState('');
  const [intent, setIntent] = useState('');
  const [audioStream, setAudioStream] = useState<MediaStream | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  // Initialize WebSocket connection
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Create WebSocket connection
    const newSocket = new WebSocket('ws://localhost:8000/speech-ai');
    
    newSocket.onopen = () => {
      console.log('WebSocket connection established');
    };

    newSocket.onmessage = (event) => {
      const data: SpeechProcessingResult = JSON.parse(event.data);
      
      // Update UI with processing results
      setTranscription(data.transcription);
      setLanguage(data.language);
      setIntent(data.intent);
      setResponse(data.response);

      // Play audio response if available
      if (data.audioResponse) {
        const audio = new Audio(data.audioResponse);
        audio.play();
      }
    };

    newSocket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    setSocket(newSocket);

    // Cleanup on component unmount
    return () => {
      newSocket.close();
    };
  }, []);

  const startRecording = async () => {
    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioStream(stream);

      // Create media recorder
      const recorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });

      recorder.ondataavailable = async (event) => {
        if (event.data.size > 0 && socket) {
          // Send audio chunk to backend via WebSocket
          const arrayBuffer = await event.data.arrayBuffer();
          socket.send(arrayBuffer);
        }
      };

      recorder.start(100); // Send chunks every 100ms
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      
      // Stop all tracks in the audio stream
      if (audioStream) {
        audioStream.getTracks().forEach(track => track.stop());
      }

      setIsRecording(false);
      setAudioStream(null);
      setMediaRecorder(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-white shadow-md rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">
          Multilingual Speech AI
        </h1>

        {/* Recording Controls */}
        <div className="flex justify-center space-x-4 mb-6">
          {!isRecording ? (
            <button 
              onClick={startRecording}
              className="bg-blue-500 text-white p-3 rounded-full hover:bg-blue-600 transition"
              aria-label="Start Recording"
            >
              <Mic size={24} />
            </button>
          ) : (
            <button 
              onClick={stopRecording}
              className="bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition"
              aria-label="Stop Recording"
            >
              <StopCircle size={24} />
            </button>
          )}
        </div>

        {/* Results Display */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Transcription
            </label>
            <p className="mt-1 p-2 bg-gray-50 rounded">{transcription || 'No transcription yet'}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Language
            </label>
            <p className="mt-1 p-2 bg-gray-50 rounded">{language || 'Not detected'}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Intent
            </label>
            <p className="mt-1 p-2 bg-gray-50 rounded">{intent || 'No intent detected'}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Response
            </label>
            <p className="mt-1 p-2 bg-gray-50 rounded">{response || 'Waiting for response'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpeechAIInterface;
