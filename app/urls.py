from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='LolWin-home'),
    path('weekly/', views.weekly, name='LolWin-weekly'),
    path('champion/', views.champions, name="LolWin-champion")
]
