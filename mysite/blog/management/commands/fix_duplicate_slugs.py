from django.core.management.base import BaseCommand
from blog.models import Post
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Fix duplicate slugs so migrations work with unique_for_date"

    def handle(self, *args, **kwargs):
        seen = {}
        for post in Post.objects.all().order_by("publish"):
            key = (post.slug, post.publish.date())
            if key in seen:
                new_slug = f"{slugify(post.slug)}-{post.id}"
                self.stdout.write(f"Changing slug '{post.slug}' → '{new_slug}'")
                post.slug = new_slug
                post.save(update_fields=["slug"])
            else:
                seen[key] = post.id
        self.stdout.write(self.style.SUCCESS("✅ All duplicate slugs fixed!"))