from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=180)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password_hash", models.CharField(max_length=256)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "auth_customers"},
        )
    ]
