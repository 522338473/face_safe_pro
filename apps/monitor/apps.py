from django.apps import AppConfig


class MonitorConfig(AppConfig):
    name = "monitor"
    verbose_name = "重点人员"

    def ready(self):
        import monitor.signals
