from django.apps import AppConfig


class DeviceConfig(AppConfig):
    name = "device"
    verbose_name = "设备管理"

    def ready(self):
        import device.signals
