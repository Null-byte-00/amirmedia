from .models import Post
from django import forms
from .models import Comment
from taggit.forms import TagField, TextareaTagWidget


class Postform(forms.ModelForm):
    tags = TagField(required=False)
    class Meta:
        model = Post
        fields = [
            'title',
            'picture',
            'text',
            'tags',
        ]


class Commentform(forms.ModelForm):
    post_id = forms.IntegerField()

    class Meta:
        model = Comment
        fields = [
            'post_id',
            'text',
        ]