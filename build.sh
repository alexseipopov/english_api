flask db upgrade
exec gunicorn -b 0.0.0.0:3015 run:app