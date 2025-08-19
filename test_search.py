#!/usr/bin/env python
"""
Test script for PostgreSQL full-text search functionality
"""
import os
import sys
import django

# Add the mysite directory to Python path
sys.path.append('/Users/muhammadhussainkadiwal/Documents/Jangi/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

def test_simple_search():
    """Test simple search against a single field"""
    print("=== Testing Simple Search ===")
    results = Post.objects.filter(title__search='django')
    print(f"Simple search for 'django' in title: {results.count()} results")
    for post in results[:3]:
        print(f"  - {post.title}")
    print()

def test_multi_field_search():
    """Test search against multiple fields"""
    print("=== Testing Multi-Field Search ===")
    results = Post.objects.annotate(
        search=SearchVector('title', 'body'),
    ).filter(search='django')
    print(f"Multi-field search for 'django': {results.count()} results")
    for post in results[:3]:
        print(f"  - {post.title}")
    print()

def test_stemming_and_ranking():
    """Test search with stemming and ranking"""
    print("=== Testing Stemming and Ranking ===")
    search_vector = SearchVector('title', 'body')
    search_query = SearchQuery('django')
    results = Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by('-rank')
    
    print(f"Ranked search for 'django': {results.count()} results")
    for post in results[:3]:
        print(f"  - {post.title} (rank: {post.rank:.3f})")
    print()

def test_weighted_search():
    """Test search with weighted vectors"""
    print("=== Testing Weighted Search ===")
    search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
    search_query = SearchQuery('django')
    results = Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.3).order_by('-rank')
    
    print(f"Weighted search for 'django': {results.count()} results")
    for post in results[:3]:
        print(f"  - {post.title} (rank: {post.rank:.3f})")
    print()

def test_trigram_similarity():
    """Test trigram similarity search"""
    print("=== Testing Trigram Similarity ===")
    results = Post.published.annotate(
        similarity=TrigramSimilarity('title', 'django'),
    ).filter(similarity__gt=0.1).order_by('-similarity')
    
    print(f"Trigram search for 'django': {results.count()} results")
    for post in results[:3]:
        print(f"  - {post.title} (similarity: {post.similarity:.3f})")
    print()

def test_typo_search():
    """Test search with typos using trigram"""
    print("=== Testing Typo Search (trigram) ===")
    results = Post.published.annotate(
        similarity=TrigramSimilarity('title', 'djano'),  # typo in 'django'
    ).filter(similarity__gt=0.1).order_by('-similarity')
    
    print(f"Trigram search for 'djano' (typo): {results.count()} results")
    for post in results[:3]:
        print(f"  - {post.title} (similarity: {post.similarity:.3f})")
    print()

def show_all_posts():
    """Show all available posts"""
    print("=== All Available Posts ===")
    posts = Post.published.all()
    print(f"Total published posts: {posts.count()}")
    for i, post in enumerate(posts[:10], 1):
        print(f"{i:2d}. {post.title}")
    if posts.count() > 10:
        print(f"    ... and {posts.count() - 10} more")
    print()

if __name__ == "__main__":
    print("PostgreSQL Full-Text Search Test")
    print("=" * 40)
    
    show_all_posts()
    test_simple_search()
    test_multi_field_search()
    test_stemming_and_ranking()
    test_weighted_search()
    test_trigram_similarity()
    test_typo_search()
    
    print("All tests completed!")
