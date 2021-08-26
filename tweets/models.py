from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="", null=True)
    image = models.FileField(upload_to='images/', blank=True)
 
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.content)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }