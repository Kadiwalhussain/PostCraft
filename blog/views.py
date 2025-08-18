# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


# ------------------------------
# Post list view (with pagination)
# ------------------------------
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts per page
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})


# ------------------------------
# Post detail view (with comments)
# ------------------------------
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # Active comments
    comments = post.comments.filter(active=True)
    # Empty comment form
    form = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
    )


# ------------------------------
# Share a post via email
# ------------------------------
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject,
                message,
                'colabhussain@gmail.com',  # your email
                [cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {'post': post, 'form': form, 'sent': sent}
    )


# ------------------------------
# Handle comment form submission
# ------------------------------
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return render(
            request,
            'blog/post/comment.html',
            {'post': post, 'form': form, 'comment': comment}
        )
    else:
        comments = post.comments.filter(active=True)
        return render(
            request,
            'blog/post/detail.html',
            {'post': post, 'comments': comments, 'form': form}
        )