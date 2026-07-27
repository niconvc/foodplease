"""Rutas del módulo de menú.

Migración desde el ejemplo: `django.conf.urls.url` fue eliminado en Django 4.0.
Se reemplaza por `path`, que además evita las expresiones regulares del
original a favor de conversores de tipo (`<int:pk>`), más legibles y que
validan el tipo del parámetro antes de llegar a la vista.
"""

from django.urls import include, path

from apps.menu import views

app_name = 'menu'

producto_patterns = [
    path('', views.producto_list, name='home'),
    path('crear/', views.producto_create, name='producto-create'),
    path('<int:pk>/', views.producto_detail, name='producto-detail'),
    path('<int:pk>/editar/', views.producto_update, name='producto-edit'),
    path('<int:pk>/eliminar/', views.producto_delete, name='producto-delete'),
    path('<int:pk>/disponibilidad/', views.producto_toggle, name='producto-toggle'),
]

categoria_patterns = [
    path('', views.categoria_list, name='categoria-list'),
    path('crear/', views.categoria_create, name='categoria-create'),
    path('<int:pk>/editar/', views.categoria_update, name='categoria-edit'),
    path('<int:pk>/eliminar/', views.categoria_delete, name='categoria-delete'),
]

urlpatterns = [
    path('', views.log_in, name='log-in'),
    path('salir/', views.log_out, name='log-out'),
    path('productos/', include(producto_patterns)),
    path('categorias/', include(categoria_patterns)),
]
