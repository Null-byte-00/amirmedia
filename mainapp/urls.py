from . import views
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signin/', views.Signin.as_view(), name='signin'),
    path('signout/', views.signout, name='signout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('', views.home, name='home'),
]
