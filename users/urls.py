from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'password_reset_request/',
        views.password_reset_request_view,
        name='password_reset_request'
    ),
    path('password_reset', views.password_reset_view, name='password_reset')
]
