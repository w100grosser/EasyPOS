cd EasyPOS
git pull origin main
python3.6 manage.py migrate
python3.6 manage.py createsuperuser --noinput --username admin --email admin@admin.com