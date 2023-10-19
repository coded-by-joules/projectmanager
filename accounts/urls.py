from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',auth_views.LoginView.as_view(template_name="registration/login.html",authentication_form=UserLoginForm), name="login"),
    path('logout/',auth_views.LogoutView.as_view())
]