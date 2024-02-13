from django.db import models

# Create your models here.

# If a prediction DNE from the LSTM output for this day, predicted_closing_price will be null.


class Stock(models.Model):
    stock_symbol = models.CharField(max_length=120)
    full_name = models.TextField()
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_closing_price = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_closing_price = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)

    def _str_(self):
        return self.title

# Add adjusted close?
class PastStockMetric(models.Model):
    stock_symbol = models.CharField(max_length=120)
    date = models.DateField()
    full_name = models.TextField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['stock_symbol', 'date'], name='unique_daily_stock_metric'
            )
        ]

    def _str_(self):
        return self.title


class PredictedStockMetric(models.Model):
    stock_symbol = models.CharField(max_length=120)
    date = models.DateField()
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Stock Symbol, Date Ran, specs. ie) MSFT_11-03-2023_univariate_forecasted
    model_reference = models.CharField(max_length=120)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['stock_symbol', 'date', 'close_price', 'model_reference'], name='unique_daily_stock_prediction'
            )
        ]

    def _str_(self):
        return self.title


class ModelExecution(models.Model):
    model_reference = models.CharField(max_length=120, primary_key=True)
    date_executed = models.DateField()
    neuron_count = models.IntegerField()
    error_method = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    rmse = models.DecimalField(max_digits=10, decimal_places=8)

    def _str_(self):
        return self.title


class Playlist(models.Model):
    user = models.CharField(max_length=120)
    playlist_name = models.CharField(max_length=120)
    stock_symbol = models.CharField(max_length=120)
    volume = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'playlist_name', 'stock_symbol'], name='unique_playlist_item'
            )
        ]

    def _str_(self):
        return self.title



# 1.  10 day simple moving average (SMA) closing price
# 2.  50 day simple moving average (SMA) closing price
# 3.  200 day simple moving average (SMA) closing price
# 4.  10 day weighted moving average (WMA) closing price
# 5.  50 day weighted moving average (WMA) closing price
# 6.  200 day weighted moving average (WMA) closing price
# 7.  10 day exponential moving average (EMA) closing price
# 8.  50 day exponential moving average (EMA) closing price
# 9.  200 day exponential moving average (EMA) closing price
# 10. Current volume
# 11. 200 day simple moving average (SMA) volume
# 12. 14 Day Relative Strength Index (RSI)
# 13. 20 Day Commodity Channel Index (CCI)
# 14. Accumulation Distribution (AD)
# 15. Fast Stochastic K%
# 16. Slow Stochastic K%
# 17. Fast Stochastic D%
# 18. Slow Stochastic D%
# 19. Moving Average Convergence \ Divergence (MACD)
class TechnicalIndicators(models.Model):
    stock_symbol = models.CharField(max_length=120, primary_key=True)
    date = models.DateField()
    ten_day_closing_sma = models.DecimalField(max_digits=16, decimal_places=8)
    fifty_day_closing_sma = models.DecimalField(max_digits=16, decimal_places=8)
    twohundred_day_closing_sma = models.DecimalField(max_digits=16, decimal_places=8)
    ten_day_closing_wma = models.DecimalField(max_digits=16, decimal_places=8)
    fifty_day_closing_wma = models.DecimalField(max_digits=16, decimal_places=8)
    twohundred_day_closing_wma = models.DecimalField(max_digits=16, decimal_places=8)
    ten_day_closing_ema = models.DecimalField(max_digits=16, decimal_places=8)
    fifty_day_closing_ema = models.DecimalField(max_digits=16, decimal_places=8)
    twohundred_day_closing_ema = models.DecimalField(max_digits=16, decimal_places=8)
    twohundred_day_volume_sma = models.DecimalField(max_digits=16, decimal_places=8)
    fourteen_day_rsi = models.DecimalField(max_digits=16, decimal_places=8)
    twenty_day_cci = models.DecimalField(max_digits=16, decimal_places=8)
    fast_k = models.DecimalField(max_digits=16, decimal_places=8)
    slow_k = models.DecimalField(max_digits=16, decimal_places=8)
    fast_d = models.DecimalField(max_digits=16, decimal_places=8)
    slow_d = models.DecimalField(max_digits=16, decimal_places=8)
    macd = models.DecimalField(max_digits=16, decimal_places=8)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['stock_symbol', 'date'], name='unique_daily_stock_technical_indicators'
            )
        ]

    def _str_(self):
        return self.title