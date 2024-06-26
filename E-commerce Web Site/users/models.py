from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "profile"
        verbose_name_plural = "profile"
    
    def __str__(self):
        return self.user.username