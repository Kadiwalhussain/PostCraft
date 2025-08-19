from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control'
        })
    )
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'recipient@example.com',
            'class': 'form-control'
        })
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Optional comments about this post...',
            'rows': 4,
            'class': 'form-control'
        })
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('weighted', 'Weighted Search (Recommended)'),
        ('simple', 'Simple Search'),
        ('trigram', 'Trigram Similarity (Good for typos)'),
    ]
    
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter search terms...',
            'class': 'form-control'
        })
    )
    search_type = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        initial='weighted',
        widget=forms.Select(attrs={'class': 'form-control'})
    )