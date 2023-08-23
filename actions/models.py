from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE,related_name="actions")
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    # adding content type to the model so we can be able to have diifernet forieign relation to various models and not only one model
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,blank=True)
    target = GenericForeignKey('target_ct', 'target_id')
    
    class Meta:
        ordering=["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=['target_ct', 'target_id']),
        ]