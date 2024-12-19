from django.urls import path

from . import views
# Create your urlpatterns here

"""
Паттерн для осуществления навигации по телу
приложения robots
"""
app_name = 'robots'

urlpatterns = [
    path('', views.total_robots_serial_in_db, name='robots'),
    path('models/', views.robot_models_in_db, name='models'),
    path('models/<int:pk>/', views.model_versions_in_db, name='model_versions'),
    path('models/<int:pk>/versions/', views.versions_in_db, name='versions'),
    path('models/<int:pk>/versions/<int:id>/', views.serial_number_in_db, name='serial'),
    path('robots/', views.robots_production, name='production'),
    path('robots/offers/', views.robots_offers, name='offers'),
    path('robots/releases/', views.robots_releases, name='releases'),
    path('robots/week/', views.week_report, name='week-report'),
]
