"""Configuración de URLs raíz del proyecto.

Corrección respecto del ejemplo: la última línea del original era
`urlpatterns + static(...)`, una expresión sin asignación cuyo resultado se
descartaba. Los archivos servidos por esa llamada nunca quedaban registrados.
Además referenciaba `settings.STATIC_ROOT`, que no estaba definido.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.menu.urls')),
]

# Solo en desarrollo: en producción los archivos subidos los sirve el
# servidor web, no Django.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
