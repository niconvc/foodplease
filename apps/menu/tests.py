"""Pruebas del módulo de menú.

Cada prueba verifica una de las correcciones aplicadas sobre el ejemplo
original o una regla de negocio de la propuesta.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto
from .services import CategoriaService, ProductoService, ReglaNegocioError


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('encargado', password='clave-segura-123')
        self.client.login(username='encargado', password='clave-segura-123')
        self.categoria = Categoria.objects.create(name='Platos de fondo', orden=2)
        self.producto = Producto.objects.create(
            name='Lomo a lo pobre',
            description='Lomo con papas fritas, cebolla y huevo.',
            precio=9990,
            categoria=self.categoria,
        )


class ProductoCrudTest(BaseTestCase):

    def test_listado_requiere_autenticacion(self):
        self.client.logout()
        respuesta = self.client.get(reverse('menu:home'))
        self.assertEqual(respuesta.status_code, 302)

    def test_crear_producto(self):
        respuesta = self.client.post(reverse('menu:producto-create'), {
            'name': 'Empanada de pino',
            'description': 'Empanada horneada de carne, cebolla y aceituna.',
            'precio': 2500,
            'categoria': self.categoria.pk,
            'disponible': True,
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Producto.objects.filter(name='Empanada de pino').exists())

    def test_editar_producto(self):
        self.client.post(
            reverse('menu:producto-edit', kwargs={'pk': self.producto.pk}),
            {
                'name': 'Lomo a lo pobre grande',
                'description': self.producto.description,
                'precio': 12990,
                'categoria': self.categoria.pk,
                'disponible': True,
            },
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.precio, 12990)

    def test_eliminar_no_procede_por_get(self):
        """El GET solo muestra la confirmación; no debe borrar el registro."""
        self.client.get(reverse('menu:producto-delete', kwargs={'pk': self.producto.pk}))
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_eliminar_procede_por_post(self):
        self.client.post(reverse('menu:producto-delete', kwargs={'pk': self.producto.pk}))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_precio_debe_ser_positivo(self):
        respuesta = self.client.post(reverse('menu:producto-create'), {
            'name': 'Producto inválido',
            'description': 'Precio en cero.',
            'precio': 0,
            'categoria': self.categoria.pk,
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Producto.objects.filter(name='Producto inválido').exists())

    def test_busqueda_filtra_resultados(self):
        Producto.objects.create(
            name='Jugo natural', description='Jugo de frutas.',
            precio=1990, categoria=self.categoria,
        )
        respuesta = self.client.get(reverse('menu:home'), {'q': 'Jugo'})
        self.assertContains(respuesta, 'Jugo natural')
        self.assertNotContains(respuesta, 'Lomo a lo pobre')


class DisponibilidadTest(BaseTestCase):

    def test_cambiar_disponibilidad(self):
        self.assertTrue(self.producto.disponible)
        ProductoService.cambiar_disponibilidad(self.producto)
        self.producto.refresh_from_db()
        self.assertFalse(self.producto.disponible)

    def test_toggle_solo_acepta_post(self):
        respuesta = self.client.get(
            reverse('menu:producto-toggle', kwargs={'pk': self.producto.pk})
        )
        self.assertEqual(respuesta.status_code, 405)


class CategoriaTest(BaseTestCase):

    def test_crear_categoria(self):
        self.client.post(reverse('menu:categoria-create'), {'name': 'Bebidas', 'orden': 4})
        self.assertTrue(Categoria.objects.filter(name='Bebidas').exists())

    def test_no_elimina_categoria_con_productos(self):
        with self.assertRaises(ReglaNegocioError):
            CategoriaService.eliminar(self.categoria)
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())

    def test_elimina_categoria_vacia(self):
        vacia = Categoria.objects.create(name='Postres', orden=5)
        CategoriaService.eliminar(vacia)
        self.assertFalse(Categoria.objects.filter(pk=vacia.pk).exists())
