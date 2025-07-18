![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)


My first Django portfolio project - a news management website where users can create, read, update and delete news articles.

## 🚀 What this project does:

This is a news website where:
- **Visitors** can read news articles, search, and browse by topics
- **Registered users** can create their own news articles and comment
- **Admins** can manage all content through Django admin panel

## 🛠️ Technologies I used:

- **Django 5.2.4** - Python web framework
- **Bootstrap 5** - For responsive design
- **SQLite** - Database
- **HTML/CSS/JavaScript** - Frontend

## 📋 How to run this project

### 1. Download the project:
```bash
git clone https://github.com/Nataliia0809/django-news-agency.git
cd django-news-agency
```

### 2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install requirements:
```bash
pip install -r requirements.txt
```

### 4. Set up database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create admin user (optional):
```bash
python manage.py createsuperuser
```

### 6. Run the server:
```bash
python manage.py runserver
```

### 7. Open in browser:
- Main website: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## ✨ Features I built:

### 📰 News management
- Create, edit, and delete news articles
- Add images to articles
- Organize articles by topics
- Set article priority levels

### 👤 User system
- User registration and login
- Custom user profiles with experience tracking
- User can write articles and comments

### 🔍 Search & Browse
- Search articles by title or content
- Filter by topic, author, or date
- Auto-suggestions while typing

### 🎨 Design
- Mobile-friendly responsive design
- Clean, professional interface
- Easy navigation

## 🧪 Testing

I wrote 21 tests to make sure everything works correctly:
```bash
python manage.py test news
```

## 📊 Database structure

The project uses these main models:
- **Redactor** - Users who can write articles
- **Topic** - Categories for articles (Politics, Sports, etc.)
- **Newspaper** - The news articles
- **Tag** - Labels for articles
- **Comment** - User comments on articles

## 🎯 What I learned

Building this project taught me:
- Django framework basics (models, views, templates)
- Database design and relationships
- User authentication and permissions
- Frontend development with Bootstrap
- Writing tests for web applications
- Git workflow and project documentation

## 🚀 Future improvements

Things I want to add later:
- Email notifications for new articles
- Social media sharing
- Article bookmarking
- Rich text editor for writing articles

## 👤 About Me

This is my first Django project created as part of my web development learning journey. 

**Nataliia Perepeliak**
- GitHub: [@Nataliia0809](https://github.com/Nataliia0809)
- Email: nperepeliak7@gmail.com

## 📝 Project status

✅ **Completed Features:**
- Basic CRUD operations
- User authentication
- Search functionality
- Responsive design
- Test coverage

This project demonstrates my understanding of Django fundamentals and full-stack web development concepts.

---

⭐ **This is my first Django project - feedback and suggestions are welcome!**