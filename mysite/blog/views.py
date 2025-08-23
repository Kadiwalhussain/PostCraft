from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from .models import Post
from .forms import EmailPostForm
from taggit.models import Tag

def post_list(request, tag_slug=None):
    """Display a list of published posts"""
    post_list = Post.published.all()
    
    # Filter by tag if provided
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # Pagination
    paginator = Paginator(post_list, 6)  # 6 posts per page
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'blog/post/list.html', context)

def post_detail(request, year, month, day, slug):
    """Display a single post"""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    # Get related posts (safely)
    try:
        related_posts = post.get_related_posts()
    except:
        related_posts = []
    
    # Get active comments (safely)
    try:
        comments = post.comments.filter(active=True, parent=None)
    except:
        comments = []
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post/detail.html', context)

def post_search(request):
    """Search for posts"""
    query = request.GET.get('query', '')
    results = []
    
    if query:
        results = Post.published.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query) |
            Q(excerpt__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        posts = paginator.page(1)
    
    context = {
        'query': query,
        'posts': posts,
        'total_results': len(results),
    }
    return render(request, 'blog/post/search.html', context)


def post_share(request, post_id):
    """Share a post via email"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Build the email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read '{post.title}'"
            message = f"Read '{post.title}' at {post_url}\n\n" \
                     f"{cd['name']}'s comments: {cd['comments']}"
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL
                    recipient_list=[cd['to']],
                    fail_silently=False,
                )
                sent = True
                messages.success(request, f'Post was successfully shared with {cd["to"]}!')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
    else:
        form = EmailPostForm()
    
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'blog/post/share.html', context)


def post_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    if request.method == 'POST':
        # Handle comment submission
        # For now, just redirect back to the post
        messages.success(request, 'Comment functionality will be implemented soon!')
        return redirect(post.get_absolute_url())
    
    # If not POST, redirect to post detail
    return redirect(post.get_absolute_url())
