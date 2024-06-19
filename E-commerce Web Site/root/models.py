from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "product"
        verbose_name_plural = "product"
    
    def __str__(self):
        return self.name

# class Year(models.Model):
#     year = models.CharField(max_length=10)
    
#     class Meta:
#         db_table = "year"
#         verbose_name_plural = "year"
    
#     def __str__(self):
#         return self.year

# class Storage(models.Model):
#     name = models.CharField(max_length=10)
    
#     class Meta:
#         db_table = "storage"
#         verbose_name_plural = "storage"
    
#     def __str__(self):
#         return self.name

# class RAM(models.Model):
#     name = models.CharField(max_length=10)
    
#     class Meta:
#         db_table = "ram"
#         verbose_name_plural = "ram"
    
#     def __str__(self):
#         return self.name

# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     product = GenericForeignKey('content_type', 'object_id')
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
    
#     class Meta:
#         db_table = "cartitem"
#         verbose_name_plural = "cartitem"

#     def __str__(self):
#         return f'{self.quantity} of {self.product.title}'
    
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     oder_date = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = "order"
#         verbose_name_plural = "order"
        
#     def __str__(self):
#         return self.id