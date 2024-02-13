"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from stock import views

router = routers.DefaultRouter()
router.register(r'stocks', views.StockView, 'stock')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("", views.index),
    path("request", views.request),
    path("gatherStockData/", views.gatherStockData),
    path("gatherStockTechnicalIndicators/", views.gatherStockTechnicalIndicators),
    path("gatherStockQuote/", views.gatherStockQuote),
    path("directFetchFromYFinanceHistoric/", views.directFetchFromYFinanceHistoric),
    path("gatherStockIndicatorsOverPeriod/", views.gatherStockIndicatorsOverPeriod),
    path("gatherStockDataNoCache/", views.gatherStockDataNoCache),
    path("gatherAllTickerInfo/", views.gatherAllTickerInfo),
    path("gatherTickerHistory/", views.gatherTickerHistory),
    path("gatherTickerHistoryMetadata/", views.gatherTickerHistoryMetadata),
    path("gatherTickerHistoryIncludeAdjustedClose/", views.gatherTickerHistoryIncludeAdjustedClose),
    path("gatherTickerNews/", views.gatherTickerNews),
    path("getQuote/", views.getQuote),
    path("getTicker/", views.getTicker),
    path("getChartResponse/", views.getChartResponse),
]
