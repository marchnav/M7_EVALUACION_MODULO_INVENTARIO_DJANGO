from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path("", views.index, name="index"),

    # Productos
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/crear/", views.crear_producto, name="crear_producto"),
    path("productos/<int:id>/", views.detalle_producto, name="detalle_producto"),
    path("productos/<int:id>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:id>/eliminar/", views.eliminar_producto, name="eliminar_producto"),

    # Categorías
    path("categorias/", views.lista_categorias, name="lista_categorias"),
    path("categorias/crear/", views.crear_categoria, name="crear_categoria"),
    path("categorias/<int:id>/editar/", views.editar_categoria, name="editar_categoria"),
    path("categorias/<int:id>/eliminar/", views.eliminar_categoria, name="eliminar_categoria"),

    # Etiquetas
    path("etiquetas/", views.lista_etiquetas, name="lista_etiquetas"),
    path("etiquetas/crear/", views.crear_etiqueta, name="crear_etiqueta"),
    path("etiquetas/<int:id>/editar/", views.editar_etiqueta, name="editar_etiqueta"),
    path("etiquetas/<int:id>/eliminar/", views.eliminar_etiqueta, name="eliminar_etiqueta"),
]
