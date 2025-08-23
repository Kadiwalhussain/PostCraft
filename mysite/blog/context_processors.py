"""
Context processors for the blog application
"""
from django.conf import settings
from .models import Category, Post
from taggit.models import Tag
from django.db.models import Count, Q


def blog_context(request):
    """Add common blog data to all templates"""
    context = {}
    
    try:
        # Recent posts for sidebar
        context['sidebar_recent_posts'] = Post.published.all()[:5]
        
        # Popular posts
        context['sidebar_popular_posts'] = Post.published.order_by('-view_count')[:5]
        
        # Categories with post counts
        context['sidebar_categories'] = Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status=Post.Status.PUBLISHED))
        ).filter(post_count__gt=0)[:10]
        
        # Popular tags
        context['sidebar_tags'] = Tag.objects.annotate(
            post_count=Count('taggit_taggeditem_items')
        ).filter(post_count__gt=0).order_by('-post_count')[:15]
        
        # Blog settings
        context['blog_title'] = getattr(settings, 'BLOG_TITLE', 'PostCraft Blog')
        context['blog_description'] = getattr(settings, 'BLOG_DESCRIPTION', 'A modern blog platform')
        
    except Exception:
        # Fail silently if database is not ready
        pass
    
    return context
