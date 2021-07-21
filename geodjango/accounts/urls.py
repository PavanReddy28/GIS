from django.conf.urls import url
from django.contrib.auth import logout
from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/',views.logout_view, name="logout")
]