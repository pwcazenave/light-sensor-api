cd app
gunicorn --workers=1 --bind 0.0.0.0:$PORT main:app
