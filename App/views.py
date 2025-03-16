from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImageGenerationForm
from .services import LeonardoAIService
from .models import GeneratedImage
import time
# Create your views here.


def generate_image(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            model_id = form.cleaned_data['model']
            
            
            # Use Leonardo AI service
            leonardo_service = LeonardoAIService()
            generation_response = leonardo_service.generate_image(
                prompt=prompt,
                model_id=model_id,
            )
            
            if 'sdGenerationJob' in generation_response:
                generation_id = generation_response['sdGenerationJob']['generationId']
                
                # Save to database
                generated_image = GeneratedImage.objects.create(
                    prompt=prompt,
                    generation_id=generation_id,
                    model_id=model_id
                )
                
                # Redirect to results page
                return redirect('check_generation', pk=generated_image.id)
            else:
                error_msg = f"Error in image generation: {generation_response.get('error', 'Unknown error')}"
                messages.error(request, error_msg)
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = ImageGenerationForm()
    
    return render(request, 'image_generator/generate.html', {'form': form})


def check_generation(request, pk):
    generated_image = GeneratedImage.objects.get(pk=pk)
    
    # Get model name from choices
    from .choices import LEONARDO_MODELS
    model_name = dict(LEONARDO_MODELS).get(generated_image.model_id, "Unknown Model")
    
    # Check if we already have the image URL
    if not generated_image.image_url:
        leonardo_service = LeonardoAIService()
        generation_result = leonardo_service.get_generation_by_id(generated_image.generation_id)
        
        # If generation is complete
        if generation_result.get('generations_by_pk') and generation_result['generations_by_pk'].get('status') == 'COMPLETE':
            if generation_result['generations_by_pk'].get('generated_images'):
                # If multiple images were generated, get all URLs
                image_urls = [img['url'] for img in generation_result['generations_by_pk']['generated_images']]
                if image_urls:
                    # Store the first URL in the model (you could extend this to store multiple)
                    generated_image.image_url = image_urls[0]
                    generated_image.save()
    context = {
        'generated_image': generated_image,
        'model_name': model_name,
    }
    
    return render(request, 'image_generator/results.html', context)