from django.db import models
from django.contrib.auth.models import User
from root.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2 ,null=True)
    
    class Meta:
        db_table = "cartitem"
        verbose_name_plural = "cartitem"

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'