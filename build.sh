#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# load local files
if [ -f "initial_data.json" ]; then
    echo "Loading initial data..."
    python manage.py loaddata initial_data.json || echo "Failed to load initial data, continuing..."
else
    echo "initial_data.json not found, skipping data loading"
fi

# create superuser
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')" | python manage.py shell