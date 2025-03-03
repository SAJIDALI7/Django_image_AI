import requests
from django.conf import settings

class LeonardoAIService:
    BASE_URL = "https://cloud.leonardo.ai/api/rest/v1"
    
    def __init__(self):
        self.api_key = settings.API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_image(self, prompt, model_id, num_images, width=512, height=512):
        """Generate images using Leonardo AI with the specified model"""
        url = f"{self.BASE_URL}/generations"
        
        payload = {
            "prompt": prompt,
            "modelId": model_id,
            "num_images": num_images,
            "width": width,
            "height": height,
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {"error": str(e)}
    
    def get_generation_by_id(self, generation_id):
        """Get generation results by generation ID"""
        url = f"{self.BASE_URL}/generations/{generation_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {"error": str(e)}
            
    def get_available_models(self):
        """Get list of available models from Leonardo AI"""
        url = f"{self.BASE_URL}/platformModels"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {"error": str(e)}