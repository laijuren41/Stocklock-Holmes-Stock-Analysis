from django.contrib import admin
from app.models import StockInfo
from app.models import StockCompany
from app.models import Portfolio
from app.models import PredictedStock

# Register your models here.
admin.site.register(StockInfo)
admin.site.register(StockCompany)
admin.site.register(Portfolio)
admin.site.register(PredictedStock)