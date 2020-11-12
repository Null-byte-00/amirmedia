from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Profileform(UserCreationForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=(('male', 'male'), ('female', 'female'), ('other', 'other')))
    age = forms.IntegerField()
    bio = forms.CharField(max_length=100, required=False, widget=forms.Textarea)
    location = forms.CharField(max_length=50, required=False)
    profilepic = forms.ImageField(required=False)

    class Meta:
        fields = ['username', 'email', 'gender', 'age', 'bio', 'location', 'profilepic', 'password1', 'password2']
        model = User
