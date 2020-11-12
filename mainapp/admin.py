from django.contrib import admin
from .models import Profile
# Register your models here.


@admin.register(Profile)
class Profileadmin(admin.ModelAdmin):
    list_filter = ['gender', 'age']
    list_display = ['user', 'email', 'age', 'gender', 'bio', 'location', 'profilepic']
