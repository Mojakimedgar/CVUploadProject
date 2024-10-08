from django.db import models
from django.contrib.auth.models import User

class UserCV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to='cvs/')
    full_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s CV"
