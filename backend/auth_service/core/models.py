from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=180)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_customers"
