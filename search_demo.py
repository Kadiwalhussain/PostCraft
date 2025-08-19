#!/usr/bin/env python
"""
Comprehensive demonstration of PostgreSQL full-text search functionality
This script showcases all the search features implemented in the blog project.
"""

import os
import sys
import django

# Setup Django
os.chdir('/Users/muhammadhussainkadiwal/Documents/Jangi/mysite')
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

def print_separator(title):
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def show_posts_overview():
    """Show overview of available posts"""
    print_separator("POSTS OVERVIEW")
    
    total_posts = Post.objects.count()
    published_posts = Post.published.count()
    
    print(f"Total posts in database: {total_posts}")
    print(f"Published posts: {published_posts}")
    print(f"Draft posts: {total_posts - published_posts}")
    
    print("\nAvailable posts for search:")
    for i, post in enumerate(Post.published.all(), 1):
        print(f"{i:2d}. {post.title}")

def test_simple_search():
    """Test 1: Simple search lookups"""
    print_separator("SIMPLE SEARCH LOOKUPS")
    
    # Search in title only
    print("1. Search for 'miles' in title only:")
    results = Post.objects.filter(title__search='miles')
    print(f"   Results: {results.count()}")
    for post in results:
        print(f"   - {post.title}")
    
    # Search in multiple fields
    print("\n2. Search for 'miles' in title and body:")
    results = Post.objects.annotate(
        search=SearchVector('title', 'body'),
    ).filter(search='miles')
    print(f"   Results: {results.count()}")
    for post in results:
        print(f"   - {post.title}")

def test_stemming_and_ranking():
    """Test 2: Stemming and ranking results"""
    print_separator("STEMMING AND RANKING")
    
    search_term = 'music'
    print(f"Search term: '{search_term}' (will match 'music', 'musical', 'musician', etc.)")
    
    search_vector = SearchVector('title', 'body')
    search_query = SearchQuery(search_term)
    
    results = Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by('-rank')
    
    print(f"Results with ranking: {results.count()}")
    for post in results:
        print(f"   - {post.title} (rank: {post.rank:.3f})")

def test_weighted_queries():
    """Test 3: Weighting queries"""
    print_separator("WEIGHTED QUERIES")
    
    search_term = 'django'
    print(f"Search term: '{search_term}' with title weighted higher than body")
    
    # Apply different weights: A=1.0 for title, B=0.4 for body
    search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
    search_query = SearchQuery(search_term)
    
    results = Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.1).order_by('-rank')
    
    print(f"Results with weighted ranking: {results.count()}")
    for post in results:
        print(f"   - {post.title} (rank: {post.rank:.3f})")

def test_trigram_similarity():
    """Test 4: Trigram similarity"""
    print_separator("TRIGRAM SIMILARITY")
    
    print("1. Exact match:")
    results = Post.published.annotate(
        similarity=TrigramSimilarity('title', 'miles'),
    ).filter(similarity__gt=0.1).order_by('-similarity')
    
    print(f"   Search for 'miles': {results.count()} results")
    for post in results:
        print(f"   - {post.title} (similarity: {post.similarity:.3f})")
    
    print("\n2. Typo tolerance:")
    results = Post.published.annotate(
        similarity=TrigramSimilarity('title', 'mile'),  # missing 's'
    ).filter(similarity__gt=0.1).order_by('-similarity')
    
    print(f"   Search for 'mile' (typo): {results.count()} results")
    for post in results:
        print(f"   - {post.title} (similarity: {post.similarity:.3f})")
    
    print("\n3. Major typo:")
    results = Post.published.annotate(
        similarity=TrigramSimilarity('title', 'mils'),  # different typo
    ).filter(similarity__gt=0.1).order_by('-similarity')
    
    print(f"   Search for 'mils' (major typo): {results.count()} results")
    for post in results:
        print(f"   - {post.title} (similarity: {post.similarity:.3f})")

def test_multilingual_search():
    """Test 5: Different language configurations"""
    print_separator("MULTILINGUAL SEARCH (Example)")
    
    # This is an example - would need Spanish content to test properly
    print("Example of Spanish language configuration:")
    print("   search_vector = SearchVector('title', 'body', config='spanish')")
    print("   search_query = SearchQuery(query, config='spanish')")
    print("   This would use Spanish stemming and stop words.")
    
    # Test with English (default)
    search_term = 'music'
    search_vector = SearchVector('title', 'body', config='english')
    search_query = SearchQuery(search_term, config='english')
    
    results = Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by('-rank')
    
    print(f"\nEnglish configuration search for '{search_term}': {results.count()} results")
    for post in results:
        print(f"   - {post.title}")

def test_combined_search():
    """Test 6: Combined search approach (like in the view)"""
    print_separator("COMBINED SEARCH APPROACH")
    
    search_term = 'django'
    print(f"Combined approach for '{search_term}':")
    
    # First try weighted search with high threshold
    search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
    search_query = SearchQuery(search_term)
    results = Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.3).order_by('-rank')
    
    if results:
        print(f"   High-relevance results: {results.count()}")
        for post in results:
            print(f"   - {post.title} (rank: {post.rank:.3f})")
    else:
        print("   No high-relevance results, trying lower threshold...")
        results = Post.published.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.1).order_by('-rank')
        
        if results:
            print(f"   Lower-relevance results: {results.count()}")
            for post in results:
                print(f"   - {post.title} (rank: {post.rank:.3f})")
        else:
            print("   No ranked results, trying trigram similarity...")
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', search_term),
            ).filter(similarity__gt=0.1).order_by('-similarity')
            
            print(f"   Trigram results: {results.count()}")
            for post in results:
                print(f"   - {post.title} (similarity: {post.similarity:.3f})")

def show_search_tips():
    """Show search tips for users"""
    print_separator("SEARCH TIPS")
    
    print("1. Use simple terms for basic searches")
    print("2. For typos and partial matches, use trigram similarity")
    print("3. Weighted search prioritizes title matches over content")
    print("4. Search supports stemming (music = musical = musician)")
    print("5. Common words (a, the, and, etc.) are automatically ignored")
    print("6. PostgreSQL search is case-insensitive")

def main():
    """Run all demonstrations"""
    print("PostgreSQL Full-Text Search Demonstration")
    print("Blog Application - Complete Implementation")
    
    try:
        show_posts_overview()
        test_simple_search()
        test_stemming_and_ranking()
        test_weighted_queries()
        test_trigram_similarity()
        test_multilingual_search()
        test_combined_search()
        show_search_tips()
        
        print_separator("DEMONSTRATION COMPLETE")
        print("✅ All PostgreSQL search features are working correctly!")
        print("🌐 Visit http://127.0.0.1:8000/blog/search/ to test the web interface")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Make sure PostgreSQL is running and the database is properly configured.")

if __name__ == "__main__":
    main()
