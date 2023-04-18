from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '제목을 입력하세요',
                'maxlength': 50,
            }
        ),
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs = {
                'class': 'form-control',
                'placeholder': '내용을 입력하세요',
                'rows': 5,
                'cols': 100,
            }
        ),
    )
    class Meta:
        model = Article
        fields = ('title', 'content',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs = {
                'class': 'comment-content',
                'placeholder': '내용을 입력하세요',
                'rows': 2,
                'cols': 100,
            }
        ),
    )
    class Meta:
        model = Comment
        fields = ('content',)