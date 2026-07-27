"""Capa de repositorios (patrón Repository).

En el ejemplo original las vistas consultaban el ORM directamente
(`Movies.objects.all()`, `Movies.objects.get(pk=...)`). Eso acopla la capa de
presentación al mecanismo de persistencia: cualquier cambio en la forma de
consultar obliga a tocar las vistas.

Aquí las consultas se concentran en repositorios. Las vistas piden datos a
través de esta interfaz y desconocen si detrás hay un ORM, una API REST o
una consulta SQL directa.

Nota de diseño: el ORM de Django implementa Active Record, donde el modelo
también sabe persistirse. Superponer un Repository es una decisión discutible,
porque introduce una capa que Django no exige. Se adopta igualmente porque el
proyecto define en su arquitectura una API REST compartida entre los tres
actores (Sumativa 1): concentrar el acceso a datos en un único punto permite
reutilizar estas consultas desde la futura capa de API sin duplicarlas.
"""

from django.db.models import Count

from .models import Categoria, Producto


class CategoriaRepository:
    """Encapsula el acceso a datos de la entidad Categoria."""

    @staticmethod
    def listar():
        """Devuelve las categorías con el conteo de productos asociados.

        Se usa annotate para calcular el conteo en la misma consulta y evitar
        el problema N+1 que se produciría al contar dentro de la plantilla.
        """
        return Categoria.objects.annotate(cantidad=Count('productos'))

    @staticmethod
    def obtener(pk):
        return Categoria.objects.filter(pk=pk).first()

    @staticmethod
    def tiene_productos(categoria):
        return categoria.productos.exists()


class ProductoRepository:
    """Encapsula el acceso a datos de la entidad Producto."""

    @staticmethod
    def listar(busqueda=None, categoria_id=None, solo_disponibles=False):
        """Lista productos con filtros opcionales.

        Se aplica select_related sobre la categoría para resolver la relación
        en una sola consulta, en lugar de una consulta por fila al renderizar.
        """
        consulta = Producto.objects.select_related('categoria')

        if busqueda:
            consulta = consulta.filter(name__icontains=busqueda)
        if categoria_id:
            consulta = consulta.filter(categoria_id=categoria_id)
        if solo_disponibles:
            consulta = consulta.filter(disponible=True)

        return consulta

    @staticmethod
    def obtener(pk):
        return Producto.objects.select_related('categoria').filter(pk=pk).first()

    @staticmethod
    def contar_disponibles():
        return Producto.objects.filter(disponible=True).count()
