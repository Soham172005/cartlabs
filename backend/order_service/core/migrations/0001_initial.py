from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_id", models.CharField(max_length=64)),
                ("full_name", models.CharField(max_length=180)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=40)),
                ("address", models.TextField()),
                ("city", models.CharField(max_length=120)),
                ("postal_code", models.CharField(max_length=32)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(default="Order placed", max_length=40)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "orders"},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_id", models.CharField(max_length=80)),
                ("name", models.CharField(max_length=180)),
                ("image", models.URLField(max_length=500)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.PositiveIntegerField()),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="order_core.order")),
            ],
            options={"db_table": "order_items"},
        ),
    ]
