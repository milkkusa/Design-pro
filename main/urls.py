from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView   
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('application/create/', views.create_application, name='create_application'),
    path('application/<int:pk>/delete/', views.delete_application, name='delete_application'),
    path('superadmin/', views.admin_panel, name='admin_panel'),
    path('superadmin/application/<int:pk>/in-work/', views.set_in_work, name='set_in_work'),
    path('superadmin/application/<int:pk>/done/', views.set_done, name='set_done'),
    path('superadmin/categories/', views.categories, name='categories'),
    path('superadmin/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]

