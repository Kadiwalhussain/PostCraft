from django.contrib import admin
from .models import Post, Comment, Category, Newsletter, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'category', 'status', 'featured', 'publish']
    list_filter = ['status', 'created', 'publish', 'author', 'category', 'featured']
    search_fields = ['title', 'body', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    readonly_fields = ['reading_time', 'view_count']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'body')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'publish')
        }),
        ('Analytics', {
            'fields': ('reading_time', 'view_count'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    readonly_fields = ['ip_address', 'user_agent']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'confirmed', 'is_active', 'subscribed_at']
    list_filter = ['confirmed', 'is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created', 'read', 'replied']
    list_filter = ['read', 'replied', 'created']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created']
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True)
    mark_as_replied.short_description = "Mark selected messages as replied"