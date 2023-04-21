from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'description')
        labels = {
            'image': 'Фото к посту',
            'description': 'Статья к посту',
        }

class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')


class CommentForm(forms.Form):
    text = forms.CharField(max_length=200, required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Введите свой комментарий...Введите свой комментарий...Введите свой комментарий...Введите свой комментарий...'}))