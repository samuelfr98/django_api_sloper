# Generated by Django 4.2.6 on 2023-11-05 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelExecution",
            fields=[
                (
                    "model_reference",
                    models.CharField(max_length=120, primary_key=True, serialize=False),
                ),
                ("date_executed", models.DateField()),
                ("neuron_count", models.IntegerField()),
                ("error_method", models.CharField(max_length=120)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("rmse", models.DecimalField(decimal_places=8, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="PastStockMetric",
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
                ("date", models.DateField()),
                ("full_name", models.TextField()),
                ("open_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("close_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("high_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("low_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("volume", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "user",
                    models.CharField(max_length=120, primary_key=True, serialize=False),
                ),
                ("playlist_name", models.CharField(max_length=120)),
                ("stock_symbol", models.CharField(max_length=120)),
                ("volume", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="PredictedStockMetric",
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
                ("date", models.DateField()),
                ("close_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("model_reference", models.CharField(max_length=120)),
            ],
        ),
        migrations.AddConstraint(
            model_name="predictedstockmetric",
            constraint=models.UniqueConstraint(
                fields=("stock_symbol", "date", "close_price", "model_reference"),
                name="unique_daily_stock_prediction",
            ),
        ),
        migrations.AddConstraint(
            model_name="playlist",
            constraint=models.UniqueConstraint(
                fields=("user", "playlist_name", "stock_symbol"),
                name="unique_playlist_item",
            ),
        ),
        migrations.AddConstraint(
            model_name="paststockmetric",
            constraint=models.UniqueConstraint(
                fields=("stock_symbol", "date"), name="unique_daily_stock_metric"
            ),
        ),
    ]
