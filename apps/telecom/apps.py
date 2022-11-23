from django.apps import AppConfig


class TelecomConfig(AppConfig):
    name = "telecom"
    verbose_name = "大屏扩展"

    def ready(self):
        import telecom.signals
