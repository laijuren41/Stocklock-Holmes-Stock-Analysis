from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers


from . import views

router = routers.DefaultRouter()
router.register('data', views.ChartData)
router.register('predictdata', views.PredictedData)


urlpatterns = [

	path('', include(router.urls)),
    path('table/data/', views.TableData.as_view(), name='tableData'),
    path('uptrend/data/', views.UptrendData.as_view(), name='uptrendData'),
    path('downtrend/data/', views.DowntrendData.as_view(), name='downtrendData'),
    path('', include(router.urls))
    
]
