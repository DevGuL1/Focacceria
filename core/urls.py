from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('salumeria/', views.salumeria_page, name='salumeria'),
    path('lang/<str:lang>/', views.set_language, name='set_language'),
    # English routes
    path('en/', views.home, name='home_en'),
    path('en/menu/', views.menu_page, name='menu_en'),
    path('en/salumeria/', views.salumeria_page, name='salumeria_en'),
]
