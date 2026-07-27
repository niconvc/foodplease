from django.apps import AppConfig


class MenuConfig(AppConfig):
    """Configuración de la aplicación.

    Corrección respecto del ejemplo: allí `name` valía 'movies' mientras que
    en INSTALLED_APPS la aplicación se registraba como 'apps.movies'. La ruta
    debe coincidir con la del paquete real o Django no resuelve la aplicación.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.menu'
    verbose_name = 'Gestión de menú'
