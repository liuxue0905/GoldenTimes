from django.apps import AppConfig


class PortalConfig(AppConfig):
    name = 'portal'
    verbose_name = "流金岁月"

    def ready(self):
        import portal.signals
