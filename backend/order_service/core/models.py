from django.db import models


class Order(models.Model):
    user_id = models.CharField(max_length=64)
    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    address = models.TextField()
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=32)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=40, default="Order placed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_id = models.CharField(max_length=80)
    name = models.CharField(max_length=180)
    image = models.URLField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "order_items"
