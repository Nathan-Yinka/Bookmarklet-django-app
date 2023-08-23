from django import forms
from .models import Image
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
        
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
    
    
    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super().save(commit=False) #this save the file temporary and must call .save() to finally save
        
        #getting the url from the form
        image_url = self.cleaned_data["url"]
        
        if image_url:
            name = slugify(instance.title)
            extenstion = image_url.rsplit(".",1)[1].lower()
            
            #generating the image name
            image_name = f"{name}.{extenstion}"
        
            #downloading the image fromthe url using the request library
            response = requests.get(image_url)
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                instance.image.save(image_name,image_content,save=False)
        
        if commit:
            instance.save()
        
        return instance