# Generated by Django 4.2.6 on 2023-10-28 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock_symbol", models.CharField(max_length=120)),
                ("full_name", models.TextField()),
                ("date", models.DateField()),
                ("open_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("high_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("low_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "actual_closing_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "predicted_closing_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
            ],
        ),
    ]
