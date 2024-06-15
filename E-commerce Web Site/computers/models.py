from django.db import models
from mainapp.models import Category, SubCategory, Storage, RAM, Year
from django.contrib.auth.models import User

class ScreenSize(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "screen_size"
        verbose_name_plural = "screen_size"
    
    def __str__(self):
        return self.name

class OS(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "OS"
        verbose_name_plural = "OS"
    
    def __str__(self):
        return self.name

class CPU(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "CPU"
        verbose_name_plural = "CPU"
    
    def __str__(self):
        return self.name
    
class GPU(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "GPU"
        verbose_name_plural = "GPU"
    
    def __str__(self):
        return self.name

class Cooling(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "cooling"
        verbose_name_plural = "cooling"
    
    def __str__(self):
        return self.name

class LaptopBrand(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "laptop_brand"
        verbose_name_plural = "laptop_brand"
    
    def __str__(self):
        return self.name

class LaptopModel(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "laptop_model"
        verbose_name_plural = "laptop_model"
    
    def __str__(self):
        return self.name

class PCType(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "PC_type"
        verbose_name_plural = "PC_type"
    
    def __str__(self):
        return self.name

class PC(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    storage_capacity = models.ForeignKey(Storage, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE)
    screen_size = models.ForeignKey(ScreenSize, on_delete=models.CASCADE)
    operating_system = models.ForeignKey(OS, on_delete=models.CASCADE)
    cooling = models.ForeignKey(Cooling, on_delete=models.CASCADE)
    type = models.ForeignKey(PCType, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "PC"
        verbose_name_plural = "PC"
    
    def __str__(self):
        return self.title


class Laptop(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=2)
    brand = models.ForeignKey(LaptopBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(LaptopModel, on_delete=models.CASCADE)
    storage_capacity = models.ForeignKey(Storage, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE)
    screen_size = models.ForeignKey(ScreenSize, on_delete=models.CASCADE)
    operating_system = models.ForeignKey(OS, on_delete=models.CASCADE)
    announce_year = models.ForeignKey(Year, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "laptop"
        verbose_name_plural = "laptop"
    
    def __str__(self):
        return self.title

class Tablet(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=3)
    storage_capacity = models.ForeignKey(Storage, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    screen_size = models.ForeignKey(ScreenSize, on_delete=models.CASCADE)
    operating_system = models.ForeignKey(OS, on_delete=models.CASCADE)
    announce_year = models.ForeignKey(Year, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "tablet"
        verbose_name_plural = "tablet"
    
    def __str__(self):
        return self.title

class PartsOrAccessories(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "parts_or_accessories"
        verbose_name_plural = "parts_or_accessories"
    
    def __str__(self):
        return self.title