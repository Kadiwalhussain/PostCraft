from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # Homepage and post listing
    path('', views.post_list, name='post_list'),
    
    # Search functionality (must be before post patterns)
    path('search/', views.post_search, name='post_search'),
    
    # RSS Feed (must be before post patterns)
    path('feed/', LatestPostsFeed(), name='post_feed'),
    
    # Post sharing (specific post ID patterns)
    path('post/<int:post_id>/share/', views.post_share, name='post_share'),
    
    # Post comments (specific post ID patterns)
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    
    # Tag filtering
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    
    # Post detail (must be last due to broad pattern)
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
]