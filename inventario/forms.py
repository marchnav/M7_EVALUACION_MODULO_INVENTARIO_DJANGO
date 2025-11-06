from django import forms
from .models import Categoria, Etiqueta, Producto, DetalleProducto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]


class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ["nombre"]


class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ["dimensiones", "peso"]
        widgets = {
            "dimensiones": forms.TextInput(attrs={"placeholder": "Largo x Ancho x Alto"}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "categoria", "etiquetas"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }
