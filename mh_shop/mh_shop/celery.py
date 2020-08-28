
import os
from celery import Celery

# задаем переменную окружения, содержащую название файла настроек нашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mh_shop.settings')

app = Celery('mh_shop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



