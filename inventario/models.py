from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self) -> str:
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Muchos a Uno: muchos productos pertenecen a una categoría
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,  # evita borrar categoría si tiene productos
        related_name="productos",
    )
    # Muchos a Muchos: etiquetas opcionales
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name="productos")

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return f"{self.nombre} (${self.precio})"


class DetalleProducto(models.Model):
    """Relación Uno a Uno con Producto: cada producto tiene un detalle único."""
    producto = models.OneToOneField(
        "Producto", on_delete=models.CASCADE, related_name="detalle"
    )
    # Campos de ejemplo (puedes ampliar luego)
    dimensiones = models.CharField(max_length=100, blank=True, help_text="Largo x Ancho x Alto")
    peso = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, help_text="kg")

    def __str__(self) -> str:
        return f"Detalle de {self.producto.nombre}"
