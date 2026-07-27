"""Vistas del módulo de gestión de menú.

Se mantiene el enfoque de vistas basadas en funciones del ejemplo original,
para conservar la trazabilidad con la base entregada. Los cambios respecto
del ejemplo están comentados en cada punto donde se corrige un defecto.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import CategoriaForm, LoginForm, ProductoForm
from .repositories import CategoriaRepository, ProductoRepository
from .services import CategoriaService, ProductoService, ReglaNegocioError

PRODUCTOS_POR_PAGINA = 8


# ---------------------------------------------------------------------------
# Autenticación
# ---------------------------------------------------------------------------

def log_in(request):
    """Inicio de sesión del encargado del Local."""
    form = LoginForm(request.POST or None)
    context = {'message': None, 'form': form}

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('menu:home')
            context['message'] = 'El usuario ha sido desactivado.'
        else:
            context['message'] = 'Usuario o contraseña incorrecta.'

    return render(request, 'menu/login.html', context)


@login_required
def log_out(request):
    logout(request)
    return redirect('menu:log-in')


# ---------------------------------------------------------------------------
# Productos (CRUD completo)
# ---------------------------------------------------------------------------

@login_required
def producto_list(request):
    """Listado de productos con búsqueda, filtro por categoría y paginación.

    El ejemplo original devolvía `Movies.objects.all()` sin paginar: con un
    volumen realista de registros la vista se vuelve inutilizable y carga
    toda la tabla en memoria en cada petición.
    """
    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria') or None

    productos = ProductoRepository.listar(
        busqueda=busqueda,
        categoria_id=categoria_id,
    )

    paginador = Paginator(productos, PRODUCTOS_POR_PAGINA)
    pagina = paginador.get_page(request.GET.get('page'))

    context = {
        'productos': pagina,
        'pagina': pagina,
        'categorias': CategoriaRepository.listar(),
        'busqueda': busqueda,
        'categoria_id': categoria_id,
        'resumen': ProductoService.resumen_menu(),
    }
    return render(request, 'menu/producto/index.html', context)


@login_required
def producto_detail(request, pk):
    producto = ProductoRepository.obtener(pk)
    if producto is None:
        raise Http404('Este producto no existe.')
    return render(request, 'menu/producto/detail.html', {'producto': producto})


@login_required
def producto_create(request):
    form = ProductoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        producto = form.save()
        messages.success(request, 'Producto "%s" creado correctamente.' % producto.name)
        return redirect('menu:home')

    return render(request, 'menu/producto/form.html', {
        'form': form,
        'titulo': 'Nuevo producto',
    })


@login_required
def producto_update(request, pk):
    """Edición de producto.

    Corrección respecto del ejemplo: la vista original instanciaba el
    formulario solo con `request.POST`, omitiendo `request.FILES`. Como
    consecuencia la imagen de un registro no podía modificarse nunca, porque
    el archivo subido jamás llegaba al formulario.
    """
    producto = ProductoRepository.obtener(pk)
    if producto is None:
        raise Http404('Este producto no existe.')

    form = ProductoForm(
        request.POST or None,
        request.FILES or None,
        instance=producto,
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto "%s" actualizado.' % producto.name)
        return redirect('menu:home')

    return render(request, 'menu/producto/form.html', {
        'form': form,
        'titulo': 'Editar producto',
        'objeto': producto,
    })


@login_required
def producto_delete(request, pk):
    """Eliminación de producto en dos pasos: confirmación y ejecución.

    Corrección respecto del ejemplo: allí el borrado se ejecutaba con una
    petición GET desde un enlace. Un método GET debe ser seguro e idempotente;
    al no serlo, cualquier precarga del navegador, rastreador o enlace visitado
    por accidente eliminaba el registro, y además la operación quedaba fuera
    de la protección CSRF.

    GET muestra la confirmación; solo POST ejecuta el borrado.
    """
    producto = ProductoRepository.obtener(pk)
    if producto is None:
        raise Http404('Este producto no existe.')

    if request.method == 'POST':
        nombre = producto.name
        ProductoService.eliminar(producto)
        messages.success(request, 'Producto "%s" eliminado.' % nombre)
        return redirect('menu:home')

    return render(request, 'menu/producto/confirm_delete.html', {'producto': producto})


@login_required
@require_POST
def producto_toggle(request, pk):
    """Marca o desmarca un producto como disponible.

    Acción propia de FoodPlease: permite retirar de la carta un producto
    agotado sin eliminarlo ni editar el registro completo.
    """
    producto = ProductoRepository.obtener(pk)
    if producto is None:
        raise Http404('Este producto no existe.')

    disponible = ProductoService.cambiar_disponibilidad(producto)
    estado = 'disponible' if disponible else 'no disponible'
    messages.info(request, 'El producto "%s" quedó %s.' % (producto.name, estado))
    return redirect('menu:home')


# ---------------------------------------------------------------------------
# Categorías (CRUD completo)
# ---------------------------------------------------------------------------

@login_required
def categoria_list(request):
    """Listado de categorías.

    En el ejemplo original esta entidad solo tenía vista de listado: no era
    un CRUD, faltaban las operaciones de creación, edición y eliminación.
    """
    return render(request, 'menu/categoria/index.html', {
        'categorias': CategoriaRepository.listar(),
    })


@login_required
def categoria_create(request):
    form = CategoriaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        categoria = form.save()
        messages.success(request, 'Categoría "%s" creada.' % categoria.name)
        return redirect('menu:categoria-list')

    return render(request, 'menu/categoria/form.html', {
        'form': form,
        'titulo': 'Nueva categoría',
    })


@login_required
def categoria_update(request, pk):
    categoria = CategoriaRepository.obtener(pk)
    if categoria is None:
        raise Http404('Esta categoría no existe.')

    form = CategoriaForm(request.POST or None, instance=categoria)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoría "%s" actualizada.' % categoria.name)
        return redirect('menu:categoria-list')

    return render(request, 'menu/categoria/form.html', {
        'form': form,
        'titulo': 'Editar categoría',
        'objeto': categoria,
    })


@login_required
def categoria_delete(request, pk):
    """Eliminación de categoría, sujeta a la regla de negocio del servicio."""
    categoria = CategoriaRepository.obtener(pk)
    if categoria is None:
        raise Http404('Esta categoría no existe.')

    if request.method == 'POST':
        try:
            nombre = categoria.name
            CategoriaService.eliminar(categoria)
            messages.success(request, 'Categoría "%s" eliminada.' % nombre)
        except ReglaNegocioError as error:
            messages.error(request, str(error))
        return redirect('menu:categoria-list')

    return render(request, 'menu/categoria/confirm_delete.html', {'categoria': categoria})
