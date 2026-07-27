from django.contrib import admin

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'orden', 'total_productos', 'updated')
    search_fields = ('name',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name', 'categoria', 'precio', 'disponible', 'updated')
    list_filter = ('disponible', 'categoria')
    search_fields = ('name', 'description')
    list_editable = ('disponible',)
