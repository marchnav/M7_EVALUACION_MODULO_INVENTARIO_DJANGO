from django.contrib import admin
from .models import Categoria, Etiqueta, Producto, DetalleProducto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


class DetalleProductoInline(admin.StackedInline):
    model = DetalleProducto
    can_delete = False
    extra = 0


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "creado_en", "actualizado_en")
    list_filter = ("categoria", "etiquetas")
    search_fields = ("nombre", "descripcion")
    autocomplete_fields = ("categoria", "etiquetas")
    inlines = [DetalleProductoInline]
    ordering = ("nombre",)
