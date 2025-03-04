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
    