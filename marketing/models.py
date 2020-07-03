from django.db import models

# Create your models here.

class Subscribe(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
