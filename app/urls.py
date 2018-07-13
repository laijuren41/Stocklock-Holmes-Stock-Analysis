from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('stock-market/', views.stockMarketView, name='stockMarket'),
    path('stock/data/', views.stockAsJson, name='stockData'),
    path('prediction/', views.prediction, name='prediction'),
	path('portfolio/', login_required(views.PortfolioView.as_view()), name='portfolio'),
	path('delete_symbol/', views.delete_symbol, name='deleteSymbol')
]

