cd EasyPOS
git pull origin main
python3.8 manage.py migrate
python3.8 manage.py createsuperuser --noinput --username admin --email admin@admin.com