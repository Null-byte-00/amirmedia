from . import views
from django.urls import path

app_name = 'userprofile'

urlpatterns = [
    path('<slug:username>/', views.ProfileDetail.as_view(), name='profile'),
    path('<slug:username>/edit/', views.Profileedit.as_view()),
    path('', views.redirect_profile, name='rprofile'),
]
