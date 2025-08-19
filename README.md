# 🚀 PostCraft - Advanced Django Blog

A feature-rich Django blog application with PostgreSQL full-text search, email functionality, RSS feeds, and modern web interface.

![Django](https://img.shields.io/badge/Django-4.1.13-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🔍 **Advanced Search System**
- **PostgreSQL Full-Text Search** with multiple search algorithms
- **Weighted Search**: Prioritizes title matches over content
- **Simple Search**: Basic full-text search across multiple fields
- **Trigram Similarity**: Typo-tolerant search using character trigrams
- **Stemming & Ranking**: Intelligent word matching and relevance scoring
- **Multi-language Support**: Configurable for different languages

### 📧 **Email System**
- **Post Sharing**: Share blog posts via email
- **Custom SMTP Backend**: Fixed Django 4.1+ compatibility issues
- **Multiple Backends**: Console, file-based, and SMTP options
- **Gmail Integration**: Ready-to-use Gmail SMTP configuration
- **Error Handling**: Graceful error handling with user feedback

### 📡 **RSS & Syndication**
- **Rich RSS Feeds**: Complete with metadata and descriptions
- **Markdown Support**: Safe markdown rendering in feeds
- **Sitemap Generation**: SEO-friendly XML sitemaps
- **Feed Categories**: Tag-based content organization

### 🎨 **Modern Interface**
- **Responsive Design**: Mobile-friendly CSS layout
- **Clean UI**: Professional blog interface
- **Form Styling**: Enhanced forms with validation
- **Search Interface**: User-friendly search with type selection
- **Pagination**: Efficient content browsing

### 🏷️ **Content Management**
- **Tagging System**: Django-taggit integration
- **Comment System**: User comments with moderation
- **Admin Interface**: Full Django admin integration
- **Content Publishing**: Draft/published status management

## 🛠️ **Technology Stack**

- **Backend**: Django 4.1.13
- **Database**: PostgreSQL 14+ with pg_trgm extension
- **Frontend**: HTML5, CSS3, JavaScript
- **Search**: PostgreSQL full-text search
- **Email**: SMTP with Gmail integration
- **Deployment**: Production-ready configuration

## 📋 **Prerequisites**

- Python 3.13+
- PostgreSQL 14+
- Git

## 🚀 **Quick Start**

### 1. **Clone Repository**
```bash
git clone https://github.com/Kadiwalhussain/PostCraft.git
cd PostCraft
```

### 2. **Setup Virtual Environment**
```bash
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install django==4.1.13
pip install psycopg2-binary==2.9.10
pip install django-taggit
pip install markdown
```

### 4. **PostgreSQL Setup**
```bash
# Create database and user
psql
CREATE USER blog WITH PASSWORD 'your_password';
CREATE DATABASE blog OWNER blog ENCODING 'UTF8';

# Enable trigram extension
\c blog
CREATE EXTENSION pg_trgm;
\q
```

### 5. **Configure Settings**
Update `mysite/mysite/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'blog',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. **Run Migrations**
```bash
cd mysite
python manage.py migrate
```

### 7. **Load Sample Data (Optional)**
```bash
python manage.py loaddata mysite_data.json
```

### 8. **Create Superuser**
```bash
python manage.py createsuperuser
```

### 9. **Start Development Server**
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/blog/ to see your blog!

## 🔧 **Configuration**

### **Email Configuration**
Choose your email backend in `settings.py`:

**Development (Console)**:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production (Gmail)**:
```python
EMAIL_BACKEND = 'blog.email_backend.FixedSMTPBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### **Search Configuration**
Search types available:
- **Weighted Search**: Best overall relevance
- **Simple Search**: Basic full-text search
- **Trigram Similarity**: Typo-tolerant search

## 📖 **Usage**

### **Main URLs**
- **Blog Homepage**: `/blog/`
- **Search**: `/blog/search/`
- **RSS Feed**: `/blog/feed/`
- **Admin**: `/admin/`
- **Sitemap**: `/sitemap.xml`

### **Testing Email**
```bash
python manage.py test_email --to recipient@example.com
```

### **Search Examples**
- Visit `/blog/search/`
- Try different search types
- Test typo tolerance with trigram search

## 📁 **Project Structure**

```
PostCraft/
├── mysite/                     # Main Django project
│   ├── blog/                   # Blog application
│   │   ├── management/         # Custom management commands
│   │   ├── migrations/         # Database migrations
│   │   ├── static/            # CSS, JS, images
│   │   ├── templates/         # HTML templates
│   │   ├── templatetags/      # Custom template tags
│   │   ├── models.py          # Database models
│   │   ├── views.py           # View functions
│   │   ├── forms.py           # Form definitions
│   │   ├── urls.py            # URL patterns
│   │   ├── feeds.py           # RSS feed configuration
│   │   └── email_backend.py   # Custom email backend
│   ├── mysite/                # Project settings
│   │   ├── settings.py        # Main configuration
│   │   └── urls.py            # Root URL configuration
│   └── manage.py              # Django management script
├── docs/                      # Documentation files
└── README.md                  # This file
```

## 🧪 **Testing**

### **Run Tests**
```bash
python manage.py test
```

### **Check Configuration**
```bash
python manage.py check
python manage.py check --deploy
```

### **Test Search Functions**
```bash
python manage.py shell
>>> from blog.models import Post
>>> from django.contrib.postgres.search import *
# Test different search methods
```

## 🚀 **Deployment**

### **Production Checklist**
- [ ] Update `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up production database
- [ ] Configure email settings
- [ ] Collect static files
- [ ] Set up web server (Nginx/Apache)
- [ ] Configure WSGI server (Gunicorn/uWSGI)

### **Environment Variables**
Create `.env` file:
```
SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 📚 **Documentation**

- [Search Implementation Guide](SEARCH_IMPLEMENTATION.md)
- [Email Configuration Guide](EMAIL_WORKING_SOLUTION.md)
- [Bug Fixes Summary](BUG_FIXES_SUMMARY.md)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Hussain Kadiwal**
- GitHub: [@Kadiwalhussain](https://github.com/Kadiwalhussain)
- Email: colabhussain@gmail.com

## 🙏 **Acknowledgments**

- Django community for the excellent framework
- PostgreSQL team for powerful full-text search capabilities
- Contributors and testers

## 📊 **Project Stats**

- **Lines of Code**: 3,460+
- **Files**: 51
- **Features**: 15+
- **Search Methods**: 3
- **Test Coverage**: Comprehensive

---

⭐ **Star this repository if you found it helpful!**

🐛 **Found a bug? [Report it here](https://github.com/Kadiwalhussain/PostCraft/issues)**

💡 **Have a feature request? [Let us know!](https://github.com/Kadiwalhussain/PostCraft/issues)**
