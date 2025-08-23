from django import forms
from django.core.validators import MinLengthValidator
from .models import Comment, Newsletter, ContactMessage

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
                'rows': 5,
                'class': 'form-control',
                'required': True,
                'minlength': '10'
            })
        }
    
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and len(body.strip()) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        return body

class SearchForm(forms.Form):
    """Search form with enhanced styling"""
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts...',
            'class': 'form-control form-control-lg',
            'required': True
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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('This email is already subscribed to our newsletter.')
        return email

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
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 20:
            raise forms.ValidationError('Message must be at least 20 characters long.')
        return message