from django import forms
from django.core.validators import MinLengthValidator
from blog.models import Comment, Newsletter, ContactMessage

class EmailPostForm(forms.Form):
    """Enhanced email sharing form"""
    name = forms.CharField(
        max_length=25,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(attrs={
            'placeholder': 'Your full name',
            'class': 'form-control',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control',
            'required': True
        })
    )
    to = forms.EmailField(
        label='Recipient Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'recipient@example.com',
            'class': 'form-control',
            'required': True
        })
    )
    comments = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'placeholder': 'Add a personal message (optional)...',
            'rows': 4,
            'class': 'form-control',
            'maxlength': '500'
        })
    )

class CommentForm(forms.ModelForm):
    """Enhanced comment form with validation"""
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name',
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'class': 'form-control',
                'required': True
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'https://yourwebsite.com (optional)',
                'class': 'form-control'
            }),
            'body': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts...',
                'rows': 4,
                'class': 'form-control',
                'required': True,
                'minlength': '10'
            })
        }
    
    def clean_body(self):
        body = self.cleaned_data['body']
        if len(body) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        return body

class SearchForm(forms.Form):
    """Advanced search form"""
    query = forms.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts, tags, categories...',
            'class': 'form-control form-control-lg',
            'autocomplete': 'off'
        })
    )

class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    
    class Meta:
        model = Newsletter
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control',
                'required': True
            })
        }
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I agree to receive newsletter emails and can unsubscribe at any time.'
    )

class ContactForm(forms.ModelForm):
    """Contact form with enhanced validation"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'class': 'form-control',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject of your message',
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Type your message here...',
                'rows': 6,
                'class': 'form-control',
                'required': True,
                'minlength': '20'
            })
        }
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 20:
            raise forms.ValidationError('Message must be at least 20 characters long.')
        return message
