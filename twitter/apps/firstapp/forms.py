from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
"""
class PostsForm(forms.Form):
    title = forms.CharField(
        label = "Название поста", 
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
                }))

    text = forms.CharField(
        label = "Содержание поста", 
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control mt-3', 
                'rows': 3}
            ))
"""

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image')

    """def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title')
        self.text = kwargs.pop('text')
        self.image = kwargs.pop('image')
        super(PostForm, self).__init__(**kwargs)"""

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('username', 'text')

class SearchForm(forms.Form):
    query = forms.CharField(label='Запрос')
    search_title = forms.BooleanField(label='Поиск по заголовку', required=False)
    search_text = forms.BooleanField(label='Поиск по содержанию', required=False)
