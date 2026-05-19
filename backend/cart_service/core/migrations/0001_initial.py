from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_id", models.CharField(max_length=64)),
                ("product_id", models.CharField(max_length=80)),
                ("name", models.CharField(max_length=180)),
                ("image", models.URLField(max_length=500)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "cart_items", "unique_together": {("user_id", "product_id")}},
        )
    ]
