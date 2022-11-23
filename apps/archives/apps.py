from django.apps import AppConfig


class ArchivesConfig(AppConfig):
    name = "archives"
    verbose_name = "人员档案"

    def ready(self):
        import archives.signals
