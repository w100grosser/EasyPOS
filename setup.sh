cd EasyPOS
git pull origin main
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --noinput --username admin --email admin@admin.com