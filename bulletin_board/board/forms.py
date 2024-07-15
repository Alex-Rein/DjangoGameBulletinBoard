from django import forms
from tinymce.widgets import TinyMCE

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    # content = forms.Field(label='Содержимое')
    category = forms.ChoiceField(choices=Post.CATEGORIES)

    # def __init__(self, *args, user=None, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     if user is not None:
    #         self.fields['author'].initial = user.username

    class Meta:
        model = Post
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}
        fields = [
            'title',
            'content',
            'category',
        ]
