"""
Utility functions for the blog application
"""
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count, Sum, Avg
from datetime import timedelta


def get_client_ip(request):
    """Get the client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_post_view(request, post):
    """Track post view for analytics"""
    from .models import PostView
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user = request.user if request.user.is_authenticated else None
    
    # Check if this IP already viewed this post today
    today = timezone.now().date()
    cache_key = f'post_view_{post.id}_{ip_address}_{today}'
    
    if not cache.get(cache_key):
        # Create view record
        PostView.objects.create(
            post=post,
            ip_address=ip_address,
            user_agent=user_agent,
            user=user
        )
        
        # Increment view count
        post.view_count += 1
        post.save(update_fields=['view_count'])
        
        # Cache this view for 24 hours
        cache.set(cache_key, True, 86400)


def generate_sitemap():
    """Generate XML sitemap for SEO"""
    from .models import Post
    from django.urls import reverse
    from django.utils import timezone
    
    posts = Post.published.all()
    sitemap_data = {
        'posts': posts,
        'last_updated': timezone.now(),
        'base_url': getattr(settings, 'BASE_URL', 'http://localhost:8000')
    }
    return sitemap_data


def send_newsletter_email(subscriber_email, post):
    """Send newsletter email for new posts"""
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    
    try:
        context = {
            'post': post,
            'base_url': getattr(settings, 'BASE_URL', 'http://localhost:8000')
        }
        
        html_content = render_to_string('blog/email/newsletter.html', context)
        text_content = render_to_string('blog/email/newsletter.txt', context)
        
        subject = f'New Post: {post.title}'
        
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        return True
    except Exception as e:
        print(f"Newsletter email error: {e}")
        return False


def get_reading_stats():
    """Get reading statistics for dashboard"""
    from .models import Post, PostView
    from django.db.models import Count, Sum
    
    cache_key = 'reading_stats'
    stats = cache.get(cache_key)
    
    if not stats:
        stats = {
            'total_posts': Post.published.count(),
            'total_views': PostView.objects.count(),
            'total_reading_time': Post.published.aggregate(
                total=Sum('reading_time')
            )['total'] or 0,
            'avg_reading_time': Post.published.aggregate(
                avg=Avg('reading_time')
            )['avg'] or 0,
        }
        
        # Cache for 1 hour
        cache.set(cache_key, stats, 3600)
    
    return stats


def get_popular_content():
    """Get popular content for recommendations"""
    from .models import Post
    
    cache_key = 'popular_content'
    content = cache.get(cache_key)
    
    if not content:
        # Get posts from last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        content = {
            'trending_posts': Post.published.filter(
                publish__gte=thirty_days_ago
            ).order_by('-view_count')[:5],
            
            'most_commented': Post.published.annotate(
                comment_count=Count('comments')
            ).order_by('-comment_count')[:5],
            
            'recently_updated': Post.published.order_by('-updated')[:5]
        }
        
        # Cache for 30 minutes
        cache.set(cache_key, content, 1800)
    
    return content


def generate_og_image(post):
    """Generate Open Graph image for social sharing"""
    # This would integrate with a service like Canvas API or similar
    # For now, return a placeholder
    return f"https://via.placeholder.com/1200x630/007bff/ffffff?text={post.title[:50]}"


def analyze_content_sentiment(text):
    """Basic sentiment analysis of content"""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
    
    text_lower = text.lower()
    positive_count = sum(word in text_lower for word in positive_words)
    negative_count = sum(word in text_lower for word in negative_words)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'


def get_search_suggestions(query):
    """Get search suggestions based on query"""
    from .models import Post
    from taggit.models import Tag
    
    suggestions = []
    
    # Get matching post titles
    posts = Post.published.filter(
        title__icontains=query
    )[:3]
    
    for post in posts:
        suggestions.append({
            'type': 'post',
            'title': post.title,
            'url': post.get_absolute_url()
        })
    
    # Get matching tags
    tags = Tag.objects.filter(
        name__icontains=query
    )[:3]
    
    for tag in tags:
        suggestions.append({
            'type': 'tag',
            'title': f'#{tag.name}',
            'url': f'/tag/{tag.slug}/'
        })
    
    return suggestions


def export_analytics_data(start_date, end_date):
    """Export analytics data for given date range"""
    from .models import PostView, Post
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['Date', 'Post Title', 'Views', 'Reading Time'])
    
    # Get views in date range
    views = PostView.objects.filter(
        timestamp__date__range=[start_date, end_date]
    ).values('post__title', 'post__reading_time', 'timestamp__date').annotate(
        view_count=Count('id')
    )
    
    for view in views:
        writer.writerow([
            view['timestamp__date'],
            view['post__title'],
            view['view_count'],
            view['post__reading_time']
        ])
    
    return output.getvalue()
