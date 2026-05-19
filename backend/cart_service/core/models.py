from django.db import models


class CartItem(models.Model):
    user_id = models.CharField(max_length=64)
    product_id = models.CharField(max_length=80)
    name = models.CharField(max_length=180)
    image = models.URLField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart_items"
        unique_together = ("user_id", "product_id")
