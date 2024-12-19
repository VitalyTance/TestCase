from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.total_orders, name='orders'),
    path('actives/', views.active_orders, name='actives'),
    path('releases/', views.realised_orders, name='releases')
]
