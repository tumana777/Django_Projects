from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "maincategory"
        verbose_name_plural = "maincategory"
        
    def __str__(self):
        return self.name
        
class Category(models.Model):
    name = models.CharField(max_length=50)
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "category"
        verbose_name_plural = "category"
        
    def __str__(self):
        return self.maincategory.name + " > " + self.name
        
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "subcategory"
        verbose_name_plural = "subcategory"
        
    def __str__(self):
        return self.category.maincategory.name + " > " + self.category.name + " > " + self.name

class Year(models.Model):
    year = models.CharField(max_length=10)
    
    class Meta:
        db_table = "year"
        verbose_name_plural = "year"
    
    def __str__(self):
        return self.year

class Storage(models.Model):
    name = models.CharField(max_length=10)
    
    class Meta:
        db_table = "storage"
        verbose_name_plural = "storage"
    
    def __str__(self):
        return self.name

class RAM(models.Model):
    name = models.CharField(max_length=10)
    
    class Meta:
        db_table = "ram"
        verbose_name_plural = "ram"
    
    def __str__(self):
        return self.name