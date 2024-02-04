from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginViewTemp, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:pk>/', views.category, name='category')
]
