"""
Custom middleware for the blog application
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from .models import Post, PostView
from .utils import get_client_ip


class ViewCountMiddleware(MiddlewareMixin):
    """Middleware to track post views"""
    
    def process_request(self, request):
        # Skip if not a post detail page
        if not request.path.count('/') >= 4:
            return None
        
        # Check if this looks like a post detail URL
        path_parts = request.path.strip('/').split('/')
        if len(path_parts) == 4:
            try:
                year, month, day, slug = path_parts
                int(year), int(month), int(day)  # Validate they are integers
                
                # This is likely a post detail view, but we'll let the view handle the actual tracking
                # to avoid duplicate database queries
                pass
            except (ValueError, IndexError):
                pass
        
        return None
