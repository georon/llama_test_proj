import asyncio
import os
import json
import chromadb
from chromadb.utils import embedding_functions

# Directory containing RAG documents
RAG_DOCS_DIR = 'rag_docs'
COLLECTION_NAME = 'my_collection'

async def main():
    # Initialize the ChromaDB client
    client = await chromadb.AsyncHttpClient()
    
    try:
        # First, let's check if the collection exists
        collections = await client.list_collections()
        collection_names = [c.name for c in collections]
        #print collection names
        print("Collection names:")  
        print(collection_names)
        # If the collection doesn't exist, create it first
        if COLLECTION_NAME not in collection_names:
            print(f"Collection '{COLLECTION_NAME}' not found. Creating a new one...")
            # For now, let's use the default embedding function
            collection = await client.create_collection(
                name=COLLECTION_NAME,
                embedding_function=embedding_functions.OllamaEmbeddingFunction(url = "http://localhost:11434", model_name = "llama3.1:8b", timeout = 60)
            )
            print("Created new collection")
            
            # Get all .txt and .md files from RAG_DOCS_DIR
            documents = []
            metadatas = []
            ids = []
            
            for filename in os.listdir(RAG_DOCS_DIR):
                if filename.endswith(('.txt', '.md')):
                    try:
                        file_path = os.path.join(RAG_DOCS_DIR, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Create a simple ID from the filename (remove extension and replace spaces with _)
                            doc_id = os.path.splitext(filename)[0].replace(' ', '_')
                            
                            # Try to load corresponding JSON metadata file
                            json_path = os.path.join(RAG_DOCS_DIR, f"{os.path.splitext(filename)[0]}.json")
                            metadata = {"source": filename}
                            
                            if os.path.exists(json_path):
                                try:
                                    with open(json_path, 'r', encoding='utf-8') as json_file:
                                        metadata.update(json.load(json_file))
                                    print(f"  Loaded metadata from {os.path.basename(json_path)}")
                                except Exception as json_error:
                                    print(f"  Error loading metadata from {json_path}: {str(json_error)}")
                            
                            documents.append(content)
                            metadatas.append(metadata)
                            ids.append(doc_id)
                            print(f"Loaded document: {filename}")
                    except Exception as e:
                        print(f"Error loading {filename}: {str(e)}")
                        continue
            
            if documents:
                await collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Added {len(documents)} documents to collection")
            else:
                print("No .txt or .md files found in the rag_docs directory")
        else:
            print("Found existing collection")
            collection = await client.get_collection(
                name=COLLECTION_NAME
            )
        
        # Now query the collection
        print("Querying collection...")
        result = await collection.query(
            query_texts=["What cars does Ron own?"]
        )
        
        print("\nQuery results:")
        print(result)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up
        print("\nEnd of program\n")

if __name__ == "__main__":
    asyncio.run(main())
