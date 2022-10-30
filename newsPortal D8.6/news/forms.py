from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5, label="Рейтинг")
    class Meta:
        model = Post
        fields = ['title', 'text', 'rating', 'post_author']
        labels = {'title': 'Название', 'text': "Текст", 'post_author': "Автор текста"}





