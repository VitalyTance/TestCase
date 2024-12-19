from django.urls import path

from . import views

app_name = 'customers'
urlpatterns = [
    path('', views.total_customers, name='customers'),
    path('<int:pk>/', views.customer_order_list, name='customer'),
]
