from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('profile/', views.profile, name='profile'),
]

