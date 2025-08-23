from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Post, Comment, Category, PostView, Newsletter, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'color_preview']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_per_page = 20
    
    def post_count(self, obj):
        from django.db.models import Count
        count = obj.posts.filter(status=Post.Status.PUBLISHED).count()
        return count
    post_count.short_description = 'Published Posts'
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background: {}; width: 20px; height: 20px; display: inline-block; border-radius: 3px;"></span>',
            obj.color
        )
    color_preview.short_description = 'Color'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'featured', 'view_count', 'publish', 'reading_time']
    list_filter = ['status', 'featured', 'category', 'created', 'publish', 'author', 'tags']
    search_fields = ['title', 'body', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['-publish']
    list_editable = ['status', 'featured']
    list_per_page = 20
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status', 'featured')
        }),
        ('Content', {
            'fields': ('excerpt', 'body', 'thumbnail', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('publish',)
        }),
        ('Analytics', {
            'fields': ('view_count', 'reading_time'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['view_count', 'reading_time']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('tags')
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f'{updated} posts were successfully marked as published.')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status=Post.Status.DRAFT)
        self.message_user(request, f'{updated} posts were successfully marked as draft.')
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} posts were successfully marked as featured.')
    make_featured.short_description = "Mark selected posts as featured"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active', 'has_replies']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    list_editable = ['active']
    list_per_page = 25
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'parent', 'name', 'email', 'website', 'active')
        }),
        ('Content', {
            'fields': ('body',)
        }),
        ('Moderation', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['ip_address', 'user_agent']
    
    def has_replies(self, obj):
        return obj.replies.exists()
    has_replies.boolean = True
    has_replies.short_description = 'Has Replies'
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} comments were unapproved.')
    unapprove_comments.short_description = "Unapprove selected comments"

@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'user', 'timestamp']
    list_filter = ['timestamp', 'post']
    search_fields = ['post__title', 'ip_address', 'user__username']
    readonly_fields = ['post', 'ip_address', 'user_agent', 'timestamp', 'user']
    list_per_page = 50
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_at', 'is_active', 'confirmed']
    list_filter = ['is_active', 'confirmed', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['confirmation_token', 'subscribed_at']
    list_per_page = 50
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscriptions were activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriptions were deactivated.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created', 'read', 'replied']
    list_filter = ['read', 'replied', 'created']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['read', 'replied']
    readonly_fields = ['created']
    list_per_page = 25
    
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'created')
        }),
        ('Content', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('read', 'replied')
        })
    )
    
    actions = ['mark_read', 'mark_replied']
    
    def mark_read(self, request, queryset):
        updated = queryset.update(read=True)
        self.message_user(request, f'{updated} messages were marked as read.')
    mark_read.short_description = "Mark selected messages as read"
    
    def mark_replied(self, request, queryset):
        updated = queryset.update(replied=True)
        self.message_user(request, f'{updated} messages were marked as replied.')
    mark_replied.short_description = "Mark selected messages as replied"

# Customize admin site
admin.site.site_header = 'PostCraft Administration'
admin.site.site_title = 'PostCraft Admin'
admin.site.index_title = 'Welcome to PostCraft Administration'