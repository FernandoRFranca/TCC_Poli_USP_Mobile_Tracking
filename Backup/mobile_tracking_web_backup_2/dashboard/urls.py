from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('dashboard/', views.dashboard_page, name='app-dashboard'),
    path('test/', views.test, name='app-test')
]
