from django.db import models
from mainapp.models import Category, Storage, RAM, Year

class SmartphoneBrand(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "smartphone_brand"
        verbose_name_plural = "smartphone_brand"
    
    def __str__(self):
        return self.name

class SmartphoneModel(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "smartphone_model"
        verbose_name_plural = "smartphone_model"
    
    def __str__(self):
        return self.name

class SmartphoneMainCamera(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "smartphone_main_camera"
        verbose_name_plural = "smartphone_main_camera"

    def __str__(self):
        return self.name
    
class SmartphoneSelfieCamera(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "smartphone_selfie_camera"
        verbose_name_plural = "smartphone_selfie_camera"

    def __str__(self):
        return self.name

class SmartphoneOS(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "smartphone_os"
        verbose_name_plural = "smartphone_os"
    
    def __str__(self):
        return self.name

class Smartphone(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=8)
    brand = models.ForeignKey(SmartphoneBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(SmartphoneModel, on_delete=models.CASCADE)
    storage_capacity = models.ForeignKey(Storage, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    main_camera = models.ForeignKey(SmartphoneMainCamera, on_delete=models.CASCADE)
    celfie_camera = models.ForeignKey(SmartphoneSelfieCamera, on_delete=models.CASCADE)
    operating_system = models.ForeignKey(SmartphoneOS, on_delete=models.CASCADE)
    announce_year = models.ForeignKey(Year, on_delete=models.CASCADE)

    class Meta:
        db_table = "smartphone"
        verbose_name_plural = "smartphone"
    
    def __str__(self):
        return self.title