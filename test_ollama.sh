#!/bin/bash
#https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/resolve/main/README.md
ollama run llama3.1:8b
cd llama_test_proj
source venv/bin/activate
nohup chroma run --path ./chromadb_data > chroma.log 2>&1 &
python3 delete_collection.py --all
python3 test_chromadb.py
python3 test_ollama.py
#ollama stop llama3.1:8b




