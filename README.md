# FoodPlease 2.0 — Módulo de gestión de menú

APTC106 — Semana 6 — Sumativa 2
Integrantes: Nicolás Duarte Maldonado — Nicolás Navarrete Caro

Este módulo corresponde a la interfaz que en la Sumativa 1 asignamos al actor
Local: una aplicación web responsive con la que gestiona los productos de su
carta. Tomamos como base el ejemplo `simple-crud-django` entregado en clases y
lo adaptamos a nuestra propuesta.

## Requisitos

- Python 3.10 o superior
- pip

## Puesta en marcha

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear la base de datos
python manage.py migrate

# 4. Cargar el menú de ejemplo
python manage.py cargar_demo

# 5. Levantar el servidor
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/> e ingresar con el usuario `encargado` y la
contraseña `foodplease2026`.

## Qué hace el módulo

| Entidad | Crear | Leer | Actualizar | Eliminar |
|---|---|---|---|---|
| Producto | Sí | Listado y detalle | Sí | Con confirmación |
| Categoría | Sí | Listado con conteo | Sí | Con regla de negocio |

Sumamos además búsqueda por nombre, filtro por categoría, paginación,
indicadores del estado del menú y un botón para marcar un producto como
agotado sin tener que editarlo entero.

## Organización del proyecto

```
manage.py
requirements.txt
crud/                       Configuración del proyecto
apps/menu/                  Aplicación del módulo de menú
    models.py               Categoria y Producto
    repositories.py         Acceso a datos
    services.py             Reglas de negocio
    forms.py                Formularios
    views.py                Vistas
    urls.py                 Rutas
    tests.py                Pruebas automatizadas
    templates/menu/         Plantillas
```

## Pruebas

```bash
python manage.py test apps.menu
```

Doce pruebas, todas aprobadas. Cubren las operaciones del CRUD, las
validaciones y las correcciones que describimos abajo.

## Qué cambiamos respecto del ejemplo

**Sobre la versión del framework.** El ejemplo venía sobre Django 1.11, sin
soporte desde 2020, y no arranca con las versiones actuales de Python. Optamos
por migrar a Django 5 en lugar de instalar un intérprete antiguo, porque
mantener el proyecto sobre una base sin soporte contradice el propósito de la
propuesta: aprovechar los recursos tecnológicos disponibles, que es justamente
la crítica que hicimos al modelo original de FoodPlease.

**Sobre el registro de archivos estáticos.** La última línea de `crud/urls.py`
sumaba las rutas sin asignar el resultado, de modo que el registro nunca
ocurría. Lo corregimos porque un error silencioso resulta más costoso que uno
visible: no falla, simplemente no hace nada.

**Sobre la edición de imágenes.** La vista de edición no recibía los archivos
enviados, por lo que la imagen de un producto no podía modificarse nunca. Es
una operación incompleta dentro del CRUD y la completamos.

**Sobre el borrado por enlace.** El ejemplo eliminaba registros con una
petición GET desde un enlace común. Decidimos separarlo en dos pasos —
confirmación y ejecución por POST — porque una operación destructiva no debe
quedar expuesta a cualquier visita accidental a la dirección.

**Sobre los campos del formulario.** El original declaraba todos los campos de
forma automática. Los enumeramos explícitamente para que ningún campo que
agreguemos más adelante quede editable sin que lo hayamos decidido.

**Sobre la clave secreta.** Estaba escrita dentro del código. La trasladamos a
una variable de entorno, ya que una clave publicada junto al proyecto pierde
por completo su función.

**Sobre el CRUD incompleto de categorías.** En el ejemplo esta entidad solo
tenía listado. Le agregamos las operaciones faltantes, junto con la regla de
que una categoría con productos asociados no puede eliminarse.

**Sobre el listado sin paginación.** Mostrar todos los registros en una sola
página genera cuellos de botella apenas el menú crece. Incorporamos paginación,
búsqueda y filtro por categoría.

**Sobre la configuración regional.** El ejemplo estaba configurado para
Colombia. Lo ajustamos a Chile, que es el contexto de nuestra propuesta.

## Alcance y limitaciones

El módulo administra el menú de un local, con el usuario autenticado como su
encargado. La operación con múltiples locales exige una entidad adicional y
aislamiento de datos por usuario, y preferimos dejarla fuera antes que
entregarla a medias.

Las interfaces del Cliente y del Repartidor que propusimos en la Sumativa 1 no
forman parte de esta entrega.

**Marco de acción futura.** Proponemos incorporar la entidad Local con su
aislamiento de datos, exponer estas mismas operaciones como API REST para
alimentar las aplicaciones del Cliente y del Repartidor, y sumar registro
histórico de cambios de precio.
