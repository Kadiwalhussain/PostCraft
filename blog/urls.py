# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post list view
    path('', views.post_list, name='post_list'),

    # Post detail view
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail,
         name='post_detail'),

    # Share post via email
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    # Add comment to a post
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]