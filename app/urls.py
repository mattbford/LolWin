from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='LolWin-home'),
    path('about/', views.about, name='LolWin-about'),
]
