import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Post


class LatestPostsFeed(Feed):
    feed_type = Rss201rev2Feed
    title = 'My Blog - Latest Posts'
    link = reverse_lazy('blog:post_list')
    description = 'Latest posts from my blog with full-text search capabilities.'
    
    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        try:
            # Safely render markdown
            html_content = markdown.markdown(item.body)
            return truncatewords_html(html_content, 30)
        except Exception:
            # Fallback to plain text if markdown fails
            return truncatewords_html(item.body, 30)

    def item_pubdate(self, item):
        return item.publish
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_guid(self, item):
        return f"blog-post-{item.id}"
    
    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username
    
    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()]
