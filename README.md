# Ollama Python Client

A Python client for interacting with Ollama's local language models.

## Prerequisites

1. Ollama must be installed and running on your system
2. Python 3.8 or higher
3. Chromadb installed and running on your system

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from ollama_client import OllamaClient

# Initialize client
client = OllamaClient()

# Get list of available models
models = client.get_models()
print("Available models:", models)

# Generate text using a model
response = client.generate("llama3.1:8b --host 127.0.0.1 --port 11434", "Hello, how are you?")
print("Response:", response)
```

## Features

- Connect to local Ollama instance
- List available models
- Generate text using models
- Stream responses
- Basic error handling

@command examples:

ollama run llama3.1:8b
cd llama_test_proj
source venv/bin/activate
nohup chroma run --path ./chromadb_data > chroma.log 2>&1 &
python3 delete_collection.py --all
python3 test_chromadb.py
python3 test_ollama.py
#ollama stop llama3.1:8b