from django.apps import AppConfig

from . import kafka


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        kafka.kafka_producer = kafka.init_kafka_producer()
