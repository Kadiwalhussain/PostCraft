from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, MaxLengthValidator
from taggit.managers import TaggableManager
import uuid
import re
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class FeaturedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.PUBLISHED,
            featured=True
        )

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        ARCHIVED = 'AR', 'Archived'

    # Basic fields
    title = models.CharField(
        max_length=250,
        validators=[MinLengthValidator(5), MaxLengthValidator(250)]
    )
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    
    # Content fields
    excerpt = models.TextField(
        max_length=300,
        help_text="Brief description of the post (max 300 characters)",
        blank=True
    )
    body = models.TextField(validators=[MinLengthValidator(100)])
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Media fields
    thumbnail = models.ImageField(
        upload_to='post_thumbnails/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Upload a thumbnail image for this post"
    )
    
    # Status and publishing
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    featured = models.BooleanField(default=False, help_text="Mark as featured post")
    
    # Timestamps
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Analytics fields
    view_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=0, help_text="Estimated reading time in minutes")
    
    # Managers
    objects = models.Manager()
    published = PublishedManager()
    featured_posts = FeaturedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.body:
            self.excerpt = self.get_excerpt(words=25)
        
        # Calculate reading time
        self.reading_time = self.calculate_reading_time()
        
        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160] if self.excerpt else self.get_excerpt(words=20)
        
        super().save(*args, **kwargs)
        
        # Optimize thumbnail after saving
        if self.thumbnail:
            self.optimize_thumbnail()

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    
    def get_thumbnail_url(self):
        """Get thumbnail URL or generate a default one"""
        if self.thumbnail:
            return self.thumbnail.url
        else:
            # Return category-based or AI-themed default thumbnails
            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural', 'openai', 'gpt']
            tech_keywords = ['technology', 'programming', 'coding', 'software', 'development']
            
            if any(keyword in self.title.lower() or keyword in self.body.lower() for keyword in ai_keywords):
                return "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop&auto=format"
            elif any(keyword in self.title.lower() or keyword in self.body.lower() for keyword in tech_keywords):
                return "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=250&fit=crop&auto=format"
            elif self.category:
                return f"https://ui-avatars.com/api/?name={self.category.name}&background={self.category.color[1:]}&color=ffffff&size=400x250"
            else:
                return "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400&h=250&fit=crop&auto=format"
    
    def get_excerpt(self, words=30):
        """Get a truncated excerpt of the post"""
        text = re.sub(r'<[^>]+>', '', self.body)
        word_list = text.split()
        if len(word_list) > words:
            return ' '.join(word_list[:words]) + '...'
        return text
    
    def calculate_reading_time(self):
        """Calculate estimated reading time in minutes"""
        if not self.body:
            return 0
        
        text = re.sub(r'<[^>]+>', '', self.body)
        word_count = len(text.split())
        # Average reading speed is 200-250 words per minute
        reading_time = max(1, round(word_count / 225))
        return reading_time
    
    def optimize_thumbnail(self):
        """Optimize thumbnail image"""
        if not self.thumbnail:
            return
        
        try:
            img = Image.open(self.thumbnail.path)
            
            # Resize if too large
            if img.width > 800 or img.height > 600:
                img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                img.save(self.thumbnail.path, optimize=True, quality=85)
        except Exception:
            pass  # Ignore optimization errors
    
    def get_related_posts(self, count=3):
        """Get related posts based on tags and category"""
        related = Post.published.filter(category=self.category).exclude(id=self.id)[:count]
        
        if related.count() < count:
            # Fill with posts having similar tags
            tag_related = Post.published.filter(
                tags__in=self.tags.all()
            ).exclude(id=self.id).distinct()[:count]
            
            # Combine and remove duplicates
            combined = list(related) + list(tag_related)
            seen = set()
            unique_related = []
            for post in combined:
                if post.id not in seen:
                    seen.add(post.id)
                    unique_related.append(post)
                if len(unique_related) >= count:
                    break
            
            return unique_related[:count]
        
        return related

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    website = models.URLField(blank=True)
    body = models.TextField(validators=[MinLengthValidator(10)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    # Moderation fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
    def get_replies(self):
        """Get all replies to this comment"""
        return self.replies.filter(active=True).order_by('created')

class PostView(models.Model):
    """Track post views for analytics"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        pass
        
    def __str__(self):
        return f'View of {self.post.title} at {self.timestamp}'

class Newsletter(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    confirmed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return f'{self.email} - {"Active" if self.is_active else "Inactive"}'

class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(validators=[MinLengthValidator(20)])
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Message from {self.name} - {self.subject}'