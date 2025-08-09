from typing import Optional, List, Dict, Any
import requests
import json

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama client.
        
        Args:
            base_url (str): The URL where Ollama is running. Defaults to http://localhost:11434
        """
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_models(self) -> List[str]:
        """
        Get list of available models from Ollama.
        
        Returns:
            List[str]: List of available model names
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.RequestException as e:
            raise Exception(f"Error getting models: {str(e)}")

    def generate(self, model: str, prompt: str, stream: bool = False) -> Any:
        """
        Generate text using a specific model.
        
        Args:
            model (str): Name of the model to use
            prompt (str): The prompt to generate from
            stream (bool): Whether to stream the response
            
        Returns:
            Any: If stream=False, returns the complete response. If stream=True, returns a generator
        """
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": stream
            }
            
            if stream:
                response = self.session.post(
                    f"{self.base_url}/api/generate",
                    json=data,
                    stream=True,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return self._stream_response(response)
            else:
                response = self.session.post(
                    f"{self.base_url}/api/generate",
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
                
        except requests.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_msg += f"\nResponse content: {e.response.text}"
                except:
                    pass
            raise Exception(f"Error generating text: {error_msg}")

    def _stream_response(self, response):
        """Generator to handle streaming responses"""
        for line in response.iter_lines():
            if line:
                try:
                    # Try to parse the JSON response
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        yield json_response['response']
                except json.JSONDecodeError:
                    # If not JSON, just yield the line as is
                    yield line.decode('utf-8')

    def create_embedding(self, model: str, input: str) -> Dict[str, Any]:
        """
        Create an embedding using a specific model.
        
        Args:
            model (str): Name of the model to use
            input (str): The input text to create embedding for
            
        Returns:
            Dict[str, Any]: The embedding response containing the embedding vector
        """
        try:
            data = {
                "model": model,
                "prompt": input
            }
            response = self.session.post(
                f"{self.base_url}/api/embeddings",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            # Ensure the response has the expected format
            if 'embedding' not in result:
                raise ValueError("Embedding not found in the API response")
            return result
        except requests.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_msg += f"\nResponse content: {e.response.text}"
                except:
                    pass
            raise Exception(f"Error creating embedding: {error_msg}")

    def create_moderation(self, model: str, input: str) -> Dict[str, Any]:
        """
        Create a moderation check using a specific model.
        
        Args:
            model (str): Name of the model to use
            input (str): The input text to moderate
            
        Returns:
            Dict[str, Any]: The moderation response
        """
        try:
            data = {
                "model": model,
                "input": input
            }
            response = self.session.post(f"{self.base_url}/api/moderate", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error creating moderation: {str(e)}")
