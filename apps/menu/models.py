"""Modelos del módulo de gestión de menú de FoodPlease 2.0.

Adaptación del ejemplo `simple-crud-django` (modelos Categories/Movies).
Se conserva la clase abstracta BaseName del original, que aplica el patrón
Template Method: define la estructura común (nombre + auditoría de fechas)
y delega en las subclases los campos específicos de cada entidad.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse_lazy


class BaseName(models.Model):
    """Clase base abstracta heredada del ejemplo original.

    Centraliza el nombre y los campos de auditoría para evitar repetirlos
    en cada entidad. Al ser abstracta no genera tabla propia.
    """

    name = models.CharField(max_length=150, verbose_name='Nombre')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Categoria(BaseName):
    """Categoría del menú: entradas, platos de fondo, bebidas, postres.

    Reemplaza a `Categories` del ejemplo. El campo `minimum_age` del original
    no aplica al rubro gastronómico y se sustituye por `orden`, que define la
    posición de la categoría en la carta mostrada al Cliente.
    """

    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden en la carta',
        help_text='Menor número aparece primero en el menú.',
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'name']

    def get_edit_url(self):
        return reverse_lazy('menu:categoria-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('menu:categoria-delete', kwargs={'pk': self.pk})

    @property
    def total_productos(self):
        return self.productos.count()


class Producto(BaseName):
    """Producto del menú que el Local ofrece al Cliente.

    Reemplaza a `Movies` del ejemplo. El campo `release_date` se sustituye por
    `precio`, y se incorpora `disponible`, que responde al problema de gestión
    de disponibilidad detectado en la Sumativa 1: cuando un producto se agota,
    el Local lo marca como no disponible y deja de ofrecerse al Cliente.
    """

    description = models.CharField(max_length=256, verbose_name='Descripción')
    precio = models.PositiveIntegerField(
        verbose_name='Precio (CLP)',
        validators=[MinValueValidator(1, 'El precio debe ser mayor que cero.')],
    )
    image = models.ImageField(
        upload_to='productos',
        verbose_name='Imagen',
        blank=True,
        null=True,
    )
    disponible = models.BooleanField(
        default=True,
        verbose_name='Disponible',
        help_text='Si se desmarca, el producto deja de ofrecerse al Cliente.',
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Categoría',
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['categoria__orden', 'name']

    def get_edit_url(self):
        return reverse_lazy('menu:producto-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('menu:producto-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse_lazy('menu:producto-detail', kwargs={'pk': self.pk})

    def get_toggle_url(self):
        return reverse_lazy('menu:producto-toggle', kwargs={'pk': self.pk})
