from django import forms
from .choices import LEONARDO_MODELS

class ImageGenerationForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Describe the image you want to generate"
    )
    model = forms.ChoiceField(
        choices=LEONARDO_MODELS,
        help_text="Select which AI model to use"
    )
    num_images = forms.IntegerField(
        min_value=1,
        max_value=4,
        initial=1,
        help_text="Number of images to generate (1-4)"
    )