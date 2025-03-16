from django.core.management.base import BaseCommand
from App.services import LeonardoAIService
import json

class Command(BaseCommand):
    help = 'Fetch and update Leonardo AI models'

    def handle(self, *args, **kwargs):
        service = LeonardoAIService()
        models = service.get_available_models()
        
        if 'error' not in models:
            model_choices = []
            for model in models.get('models', []):
                model_choices.append((model['id'], model['name']))
            
            self.stdout.write(json.dumps(model_choices, indent=2))
            self.stdout.write(self.style.SUCCESS(f'Found {len(model_choices)} models'))
        else:
            self.stdout.write(self.style.ERROR(f"Error: {models.get('error')}"))