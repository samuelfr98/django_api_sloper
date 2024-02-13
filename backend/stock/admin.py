from django.contrib import admin

from .models import Stock, PastStockMetric, PredictedStockMetric, ModelExecution, Playlist


class stock_admin(admin.ModelAdmin):
    list_display = ('stock_symbol',
                    'full_name',
                    'date',
                    'open_price',
                    'high_price',
                    'low_price',
                    'actual_closing_price',
                    'predicted_closing_price')


# Register your models here.


admin.site.register(Stock, stock_admin)
admin.site.register(PastStockMetric)
admin.site.register(PredictedStockMetric)
admin.site.register(ModelExecution)
admin.site.register(Playlist)
