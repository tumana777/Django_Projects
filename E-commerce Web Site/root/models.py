from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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
    image = models.ImageField(default="product-pictures/default.jpg", upload_to='product-pictures', null=True, blank=True)
    
    class Meta:
        db_table = "product"
        verbose_name_plural = "product"
    
    def __str__(self):
        return self.name
    
    def save(self):
        super().save()
        
        img = Image.open(self.image.path)
        
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order"
        verbose_name_plural = "order"

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "orderitem"
        verbose_name_plural = "orderitem"

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "watchlist"
        verbose_name_plural = "watchlist"
    
    def __str__(self):
        return f"{self.user} -> {self.product}"