"""Capa de servicios (patrón Service Layer).

Las reglas de negocio no viven en las vistas ni en las plantillas: se agrupan
aquí. Una vista queda reducida a recibir la petición, delegar en el servicio y
elegir qué respuesta devolver.

El beneficio concreto es que estas reglas quedan disponibles para cualquier
otro punto de entrada del sistema. En la arquitectura definida en la Sumativa 1
los tres actores comparten un mismo backend: la regla "no se puede eliminar una
categoría con productos asociados" debe cumplirse igual si la llamada llega
desde esta interfaz web o desde la API que consume la aplicación del Repartidor.
"""

from .models import Producto
from .repositories import CategoriaRepository, ProductoRepository


class ReglaNegocioError(Exception):
    """Error de regla de negocio, apto para mostrarse al usuario final."""


class CategoriaService:

    @staticmethod
    def eliminar(categoria):
        """Elimina una categoría solo si no tiene productos asociados.

        Sin esta validación la operación fallaría a nivel de base de datos por
        la restricción PROTECT de la llave foránea, devolviendo un error 500.
        Se valida antes para entregar un mensaje comprensible al Local.
        """
        if CategoriaRepository.tiene_productos(categoria):
            raise ReglaNegocioError(
                'No se puede eliminar la categoría "%s" porque tiene %d '
                'producto(s) asociado(s). Reasigne o elimine esos productos '
                'primero.' % (categoria.name, categoria.total_productos)
            )
        categoria.delete()


class ProductoService:

    @staticmethod
    def cambiar_disponibilidad(producto):
        """Invierte la disponibilidad del producto y devuelve el nuevo estado.

        Responde al problema 8 de la Sumativa 1: el Local necesita retirar un
        producto agotado de la carta de forma inmediata, sin editar el registro
        completo ni eliminarlo.
        """
        producto.disponible = not producto.disponible
        producto.save(update_fields=['disponible', 'updated'])
        return producto.disponible

    @staticmethod
    def eliminar(producto):
        producto.delete()

    @staticmethod
    def resumen_menu():
        """Indicadores para la cabecera del listado."""
        total = Producto.objects.count()
        disponibles = ProductoRepository.contar_disponibles()
        return {
            'total': total,
            'disponibles': disponibles,
            'agotados': total - disponibles,
        }
