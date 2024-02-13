from rest_framework import serializers
from .models import Stock, PastStockMetric, PredictedStockMetric, ModelExecution, Playlist


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'stock_symbol',
            'full_name',
            'date',
            'open_price',
            'high_price',
            'low_price',
            'actual_closing_price',
            'predicted_closing_price',
        )
        model = PastStockMetric
        fields = (
            'stock_symbol',
            'date',
            'full_name',
            'open_price',
            'close_price',
            'high_price',
            'low_price',
            'volume',
        )
        model = PredictedStockMetric
        fields = (
            'stock_symbol',
            'date',
            'close_price',
            'model_reference',
        )
        model = ModelExecution
        fields = (
            'model_reference',
            'date_executed',
            'neuron_count',
            'error_method',
            'start_date',
            'end_date',
            'rmse',
        )
        model = Playlist
        fields = (
            'user',
            'playlist_name',
            'stock_symbol',
            'volume',
        )
