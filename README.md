command to start server
# python manage.py runserver 

command to start celery
worker:
# celery -A stock_p.celery worker --pool=solo -l info

beat:
# celery -A stock_p beat -l INFO