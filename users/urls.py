from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('update_user/', views.update_user, name='update_user'),
    path('change_password/', views.change_password, name='change_password'),
]
