# Real-time Speech AI Model

A high-performance, multilingual real-time speech AI system built with Python, TypeScript, and C++.

## Overview

This project implements a complete real-time speech AI pipeline that can:

- Capture and preprocess audio streams with minimal latency
- Perform multilingual speech recognition
- Process natural language understanding
- Generate contextually relevant responses
- Synthesize speech output

The architecture prioritizes real-time performance while maintaining high accuracy across multiple languages.

## Architecture

![Architecture Diagram](docs/architecture.png)

The system consists of the following components:

1. **Audio Processing Module (C++)**: Handles low-level audio capture, preprocessing, and feature extraction with minimal latency.

2. **Speech Recognition Engine (Python)**: Converts audio input to text using optimized deep learning models.

3. **Natural Language Processing (Python)**: Analyzes transcribed text for intent recognition and semantic understanding.

4. **Response Generation (Python)**: Creates contextually relevant responses based on the processed input.

5. **Web Interface (TypeScript)**: Provides a responsive user interface for interacting with the system.

## Key Features

- **Real-time Processing**: Optimized for sub-200ms latency from speech to response
- **Multilingual Support**: Works across multiple languages with automatic language detection
- **Streaming Inference**: Processes audio in chunks for immediate feedback
- **Cross-platform Compatibility**: Works on desktop and mobile browsers
- **Extensible Architecture**: Modular design allows for easy component replacement

## Technical Requirements

- Python 3.10+
- Node.js 18+
- C++ compiler with C++17 support
- CUDA-compatible GPU (recommended)

## Getting Started

### Prerequisites

```bash
# Install C++ dependencies
sudo apt-get install -y portaudio19-dev libfftw3-dev

# Install Python dependencies
pip install -r requirements.txt

# Install TypeScript dependencies
npm install
```

### Running the Application

1. Start the backend services:

```bash
python src/backend/main.py
```

2. Launch the web interface:

```bash
npm run dev
```

3. Access the application at `http://localhost:3000`

## Development Workflow

### Building the C++ Components

```bash
mkdir build && cd build
cmake ..
make
```

### Training Custom Models

```bash
python src/training/train_asr.py --config configs/asr_config.yaml
```

### Running Tests

```bash
# Run backend tests
pytest tests/

# Run frontend tests
npm test
```

## Performance Optimization

The system includes several optimizations for real-time performance:

- Streaming ASR with intermediate hypothesis generation
- Voice activity detection to process only speech segments
- Parallel processing pipelines for audio and text
- Model quantization for reduced inference latency
- WebAssembly for critical browser-side processing

## Deployment

### Docker Deployment

```bash
docker-compose up -d
```

### Cloud Deployment

Terraform configurations are provided for AWS and Google Cloud Platform:

```bash
cd terraform/aws
terraform init
terraform apply
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI Whisper for the ASR foundation
- TensorFlow and PyTorch teams
- PortAudio contributors
