from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required  # 👈 import para proteger vistas

from .models import Categoria, Etiqueta, Producto, DetalleProducto
from .forms import (
    CategoriaForm,
    EtiquetaForm,
    ProductoForm,
    DetalleProductoForm,
)

# -------------------------------------------------
# Página de inicio (pública)
# -------------------------------------------------
def index(request):
    return render(request, "index.html")


# -------------------------------------------------
# Productos (CRUD) — protegidas
# -------------------------------------------------
@login_required
def lista_productos(request):
    q = request.GET.get("q")
    categoria_id = request.GET.get("categoria")
    productos = Producto.objects.select_related("categoria").prefetch_related("etiquetas").all()

    if q:
        productos = productos.filter(nombre__icontains=q)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()
    ctx = {"productos": productos, "categorias": categorias, "q": q or "", "categoria_id": categoria_id or ""}
    return render(request, "productos/lista.html", ctx)


@login_required
@transaction.atomic
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        detalle_form = DetalleProductoForm(request.POST)
        if form.is_valid() and detalle_form.is_valid():
            producto = form.save()
            # crear detalle 1:1
            DetalleProducto.objects.create(
                producto=producto,
                dimensiones=detalle_form.cleaned_data.get("dimensiones"),
                peso=detalle_form.cleaned_data.get("peso"),
            )
            messages.success(request, "Producto creado correctamente.")
            return redirect(reverse("lista_productos"))
    else:
        form = ProductoForm()
        detalle_form = DetalleProductoForm()

    return render(request, "productos/crear.html", {"form": form, "detalle_form": detalle_form})


@login_required
def detalle_producto(request, id: int):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria").prefetch_related("etiquetas"),
        pk=id,
    )
    return render(request, "productos/detalle.html", {"producto": producto})


@login_required
@transaction.atomic
def editar_producto(request, id: int):
    producto = get_object_or_404(Producto, pk=id)
    # obtener o preparar detalle
    try:
        detalle = producto.detalle
    except DetalleProducto.DoesNotExist:
        detalle = None

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        detalle_form = DetalleProductoForm(request.POST, instance=detalle)
        if form.is_valid() and detalle_form.is_valid():
            producto = form.save()
            det = detalle_form.save(commit=False)
            det.producto = producto
            det.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect(reverse("detalle_producto", args=[producto.id]))
    else:
        form = ProductoForm(instance=producto)
        detalle_form = DetalleProductoForm(instance=detalle)

    return render(
        request,
        "productos/editar.html",
        {"form": form, "detalle_form": detalle_form, "producto": producto},
    )


@login_required
@transaction.atomic
def eliminar_producto(request, id: int):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect(reverse("lista_productos"))
    return render(request, "productos/eliminar.html", {"producto": producto})


# -------------------------------------------------
# Categorías (CRUD simple) — protegidas
# -------------------------------------------------
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "categorias/lista.html", {"categorias": categorias})


@login_required
def crear_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect("lista_categorias")
    else:
        form = CategoriaForm()
    return render(request, "categorias/formulario.html", {"form": form, "modo": "crear"})


@login_required
def editar_categoria(request, id: int):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect("lista_categorias")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "categorias/formulario.html", {"form": form, "modo": "editar", "categoria": categoria})


@login_required
def eliminar_categoria(request, id: int):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == "POST":
        try:
            categoria.delete()
            messages.success(request, "Categoría eliminada correctamente.")
        except Exception:
            messages.error(request, "No se puede eliminar: hay productos asociados.")
        return redirect("lista_categorias")
    return render(request, "categorias/confirmar_eliminar.html", {"categoria": categoria})


# -------------------------------------------------
# Etiquetas (CRUD simple) — protegidas
# -------------------------------------------------
@login_required
def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, "etiquetas/lista.html", {"etiquetas": etiquetas})


@login_required
def crear_etiqueta(request):
    if request.method == "POST":
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Etiqueta creada correctamente.")
            return redirect("lista_etiquetas")
    else:
        form = EtiquetaForm()
    return render(request, "etiquetas/formulario.html", {"form": form, "modo": "crear"})


@login_required
def editar_etiqueta(request, id: int):
    etiqueta = get_object_or_404(Etiqueta, pk=id)
    if request.method == "POST":
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            messages.success(request, "Etiqueta actualizada correctamente.")
            return redirect("lista_etiquetas")
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, "etiquetas/formulario.html", {"form": form, "modo": "editar", "etiqueta": etiqueta})


@login_required
def eliminar_etiqueta(request, id: int):
    etiqueta = get_object_or_404(Etiqueta, pk=id)
    if request.method == "POST":
        etiqueta.delete()
        messages.success(request, "Etiqueta eliminada correctamente.")
        return redirect("lista_etiquetas")
    return render(request, "etiquetas/confirmar_eliminar.html", {"etiqueta": etiqueta})
