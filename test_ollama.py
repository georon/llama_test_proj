from ollama_client import OllamaClient
import asyncio
import chromadb
from chromadb.utils import embedding_functions

async def main():
    # Initialize the client
    ollama_client = OllamaClient()
    
    try:
        # Get available models
        print("Fetching available models...")
        models = ollama_client.get_models()
        print(f"Available models: {models}")
        
        if models:
            # Use the first available model for testing
            model = models[0]
            print(f"\nTesting generation with model: {model}")
            
            
            # Test embedding generation first
            # print("\n=== Testing Embedding Generation ===")
            # try:
            #     test_text = "Ron is a man who lives in Toronto. Ron owns a Toyota Venza car and another Mercedes Benz."
            #     print(f"Generating embedding for text: '{test_text}'")
                
            #     embedding = client.create_embedding(
            #         model=model,  # Using the same model as before
            #         input=test_text
            #     )
                
            #     print("\nEmbedding Generation Successful!")
            #     print(f"Model used: {embedding.get('model')}")
            #     print(f"Embedding dimensions: {len(embedding.get('embedding', []))}")
            #     print(f"First 5 dimensions: {embedding.get('embedding', [])[:5]}")
                
            # except Exception as e:
            #     print(f"Error during embedding generation: {str(e)}")
            #     print("Note: Not all models support embeddings. Make sure your model supports this feature.")
            
            # Text generation test with context
            context = "Ron is a man who lives in Toronto. Ron owns a Toyota Venza car and another Mercedes Benz."
     
            # Initialize the ChromaDB client
            chromadb_client = chromadb.HttpClient()
    
   
            # First, let's check if the collection exists
            collections = chromadb_client.list_collections()
            collection_names = [c.name for c in collections]
            #print collection names
            print("Collection names:")  
            print(collection_names)
            # If the collection doesn't exist, create it first
            if "my_collection" not in collection_names:
                # exit app with message "Collection 'my_collection' not found."
                print("Collection 'my_collection' not found.")
                exit()
            collection = chromadb_client.get_collection(
                name="my_collection"
            )

            # Now query the collection
            print("Querying collection...")
            vector_result = collection.query(
                query_texts=["What cars does Ron own?"]
            )
            
            print("\nQuery results:")
            print(vector_result)
            
            # prompt from standard input for search text
            question = input("Enter search text: ") # "How many cars does Ron have?"

            while question.lower() not in ["end", "exit", "quit"]:
                # Create a well-formatted prompt that includes the vector_result as context
                prompt = f"""Context: {vector_result['documents'][0]}
                
                Question: {question}
                
                Answer based on the context above:"""
                
                print(f"\n=== Text Generation Test ===")
                print(f"Context: {vector_result['documents'][0]}")
                print(f"Question: {question}")
                print("\nGenerating response...")
            
                # Get the response with streaming disabled
                print("\nSending request to Ollama...")
                response = ollama_client.generate(model=model, prompt=prompt, stream=False)
                
                # Print the response with better formatting
                print("\n=== Response ===")
                if isinstance(response, dict):
                    if 'response' in response:
                        print(response['response'])
                    else:
                        print("Unexpected response structure:")
                        print(response)
                else:
                    print("Unexpected response type:")
                    print(response)
                # prompt from standard input for search text
                question = input("Enter search text: ") # next question
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up
        print("\nEnd of program\n")
        
                
# removed streaming test


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
