from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_year = models.DateField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="profile-pictures", null=True, blank=True)

    class Meta:
        db_table = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return self.user.username
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)