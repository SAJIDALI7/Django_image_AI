from django.db import models

class GeneratedImage(models.Model):
    prompt = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    generation_id = models.CharField(max_length=255, blank=True, null=True)
    model_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.prompt[:50]