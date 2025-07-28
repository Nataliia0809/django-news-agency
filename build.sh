#!/usr/bin/env bash
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "📊 Running migrations..."
python manage.py migrate

echo "🗑️ Clearing existing data to avoid conflicts..."
python manage.py flush --noinput || echo "Flush failed or not needed, continuing..."

echo "📥 Loading initial data from fixtures..."
if python manage.py loaddata news_agency.initial_data --verbosity=2; then
    echo "✅ Initial data loaded successfully!"
else
    echo "❌ Failed to load initial data, but continuing with deployment..."
fi

echo "👤 Ensuring superuser exists..."
python manage.py shell << 'PYTHON_EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

# Check if any superuser exists from fixtures
if User.objects.filter(is_superuser=True).exists():
    print("✅ Superuser(s) already exist from fixtures")
else:
    # Create backup superuser only if none exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Backup superuser 'admin' created")
    else:
        print("✅ Admin user already exists")
PYTHON_EOF

echo "🎉 Build completed successfully!"