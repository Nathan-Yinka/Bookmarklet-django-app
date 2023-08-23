from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images_created")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to = "images/%Y/%m/%d")
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='images_liked', blank=True)
    
    class Meta:
        ordering=['-created']
        indexes = [
            models.Index(fields=["-created"]),
        ]
        
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            unique_slug = original_slug
            counter = 1
            while Image.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        return super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse("images:detail", kwargs={"id": self.id,"slug":self.slug})
    
            
    