from django.apps import AppConfig


class TelecomConfig(AppConfig):
    name = "apps.telecom"
    verbose_name = "大屏扩展"

    def ready(self):
        import telecom.signals
