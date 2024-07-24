from .celery import app as celery_app

__all__ = ('celery_app',)

NULLABLE = {
    'null': True,
    'blank': True,
}
