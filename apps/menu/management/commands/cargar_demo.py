"""Comando para poblar la base con el menu de demostracion.

Uso: python manage.py cargar_demo
Crea el usuario encargado y la carta de Burger Junction para probar el CRUD.
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.menu.models import Categoria, Producto

CATEGORIAS = [
    ('Hamburguesas', 1),
    ('Acompanamientos', 2),
    ('Bebidas', 3),
    ('Postres', 4),
]

# (nombre, descripcion, precio, categoria, disponible)
PRODUCTOS = [
    ('Clasica Cheddar', 'Hamburguesa de carne con queso cheddar, lechuga y tomate.', 6900, 'Hamburguesas', True),
    ('Doble Bacon', 'Doble carne con doble queso cheddar y tocino crujiente.', 8500, 'Hamburguesas', False),
    ('Crispy Onion', 'Carne con queso cheddar, cebolla crispy y salsa de la casa.', 7900, 'Hamburguesas', True),
    ('Veggie', 'Medallon de legumbres con queso, lechuga, tomate y cebolla morada.', 6500, 'Hamburguesas', True),
    ('Papas Fritas', 'Porcion de papas fritas con ketchup.', 2900, 'Acompanamientos', True),
    ('Papas Grandes', 'Porcion grande de papas fritas con ketchup.', 4200, 'Acompanamientos', True),
    ('Aros de Cebolla', 'Porcion de aros de cebolla apanados con salsa barbecue.', 4300, 'Acompanamientos', False),
    ('Nuggets de Pollo', 'Seis nuggets de pollo apanado con salsa barbecue.', 5500, 'Acompanamientos', True),
    ('Bebida Lata 350cc', 'Bebida en lata, sabores segun disponibilidad.', 1800, 'Bebidas', False),
    ('Agua Mineral', 'Botella de agua mineral 500ml.', 1500, 'Bebidas', True),
    ('Brownie con Dulce de Leche', 'Brownie casero con dulce de leche.', 2800, 'Postres', True),
]


class Command(BaseCommand):
    help = 'Carga el menu de demostracion de Burger Junction.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='encargado').exists():
            User.objects.create_superuser('encargado', 'encargado@burgerjunction.cl', 'foodplease2026')
            self.stdout.write(self.style.SUCCESS('Usuario "encargado" creado.'))

        for nombre, orden in CATEGORIAS:
            Categoria.objects.get_or_create(name=nombre, defaults={'orden': orden})

        creados = 0
        for nombre, desc, precio, categoria, disponible in PRODUCTOS:
            _, nuevo = Producto.objects.get_or_create(
                name=nombre,
                defaults={
                    'description': desc,
                    'precio': precio,
                    'categoria': Categoria.objects.get(name=categoria),
                    'disponible': disponible,
                },
            )
            creados += int(nuevo)

        self.stdout.write(self.style.SUCCESS(
            'Listo: %d categorias y %d productos nuevos.' % (len(CATEGORIAS), creados)
        ))
