from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        from . import kafka, receivers  # noqa
        kafka.kafka_producer = kafka.init_kafka_producer()
