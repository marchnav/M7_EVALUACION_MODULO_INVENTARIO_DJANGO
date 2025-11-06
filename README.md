M7_EVALUACIÓN DEL MÓDULO
INVENTARIO DJANGO + POSTGRESQL — README 
================================================

Proyecto: CRUD de Productos, Categorías, Etiquetas y Detalle 1:1
Stack: Django 5, PostgreSQL 17, django-environ
Autor: Marcelo Navarrete Y
Licencia: Uso educativo

----------------------------------------------------------------
1) OBJETIVO
----------------------------------------------------------------
Aplicación web segura para gestionar productos y sus relaciones:
- Producto: nombre, descripción, precio, categoría (M:1), etiquetas (M:M) y detalle 1:1.
- Categoría: entidad independiente (1:N con Producto).
- Etiqueta: relación muchos a muchos con Producto.
- DetalleProducto: dimensiones y peso (1:1 con Producto).
Incluye autenticación de usuario, protección CSRF y CRUD completo.

----------------------------------------------------------------
2) REQUISITOS
----------------------------------------------------------------
- Windows 10/11 con PowerShell
- Python 3.12+ y pip
- PostgreSQL 17 (servidor ejecutándose)
- Git (opcional pero recomendado)

----------------------------------------------------------------
3) CLONADO / INICIO DEL PROYECTO
----------------------------------------------------------------
# Ubícate en la carpeta de trabajo (ejemplo)
PS C:\Users\ASUS> cd C:\Users\ASUS

# Si ya tienes el repo (o lo crearás)
PS C:\Users\ASUS> git clone <URL_DEL_REPO> inventario_django
PS C:\Users\ASUS> cd .\inventario_django\

----------------------------------------------------------------
4) ENTORNO VIRTUAL E INSTALACIÓN
----------------------------------------------------------------
# Crear y activar venv
PS C:\Users\ASUS\inventario_django> py -m venv .venv
PS C:\Users\ASUS\inventario_django> .\.venv\Scripts\Activate.ps1

# Instalar dependencias
(.venv) PS ...\inventario_django> pip install -U pip
(.venv) PS ...\inventario_django> pip install django==5.2.8 psycopg[binary] django-environ

----------------------------------------------------------------
5) VARIABLES DE ENTORNO (.env)
----------------------------------------------------------------
Copia el archivo .env.example a .env y completa los valores.

Contenido sugerido para .env:
------------------------------------------------
SECRET_KEY=<token_generado_con_secrets.token_urlsafe>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
TIME_ZONE=America/Santiago
LANGUAGE_CODE=es-cl

# Ajusta usuario/password/host/puerto/nombre_db
DATABASE_URL=postgres://inventario_user:TU_PASSWORD@localhost:5432/inventario
------------------------------------------------

Generar SECRET_KEY desde PowerShell con venv activo:
(.venv) PS ...\inventario_django> python - << 'PY'
import secrets; print(secrets.token_urlsafe(64))
PY

----------------------------------------------------------------
6) POSTGRESQL — CREAR USUARIO Y BASE
----------------------------------------------------------------
# Abrir psql (si no tienes psql en PATH, añade C:\Program Files\PostgreSQL\17\bin)
PS> "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -h localhost -p 5432 -d postgres

-- Dentro de psql:
CREATE ROLE inventario_user LOGIN PASSWORD 'TU_PASSWORD';
CREATE DATABASE inventario OWNER inventario_user;
\q

Si psql no se reconoce:
PS> $env:Path = "$env:Path;C:\Program Files\PostgreSQL\17\bin"
PS> psql --version

Problemas de autenticación local (Windows): revisar C:\Program Files\PostgreSQL\17\data\pg_hba.conf.
Temporalmente permitir:
  host  all  all  127.0.0.1/32  trust
  host  all  all  ::1/128       trust
Reiniciar servicio y luego volver a scram-sha-256 tras cambiar contraseñas.

----------------------------------------------------------------
7) MIGRACIONES Y SUPERUSUARIO
----------------------------------------------------------------
(.venv) PS ...\inventario_django> python manage.py migrate
(.venv) PS ...\inventario_django> python manage.py createsuperuser

----------------------------------------------------------------
8) EJECUCIÓN
----------------------------------------------------------------
(.venv) PS ...\inventario_django> python manage.py runserver
Abrir: http://127.0.0.1:8000/

Rutas principales:
- /                      Inicio (pública)
- /productos/            Lista (requiere login)
- /productos/crear/      Crear
- /productos/<id>/       Detalle
- /productos/<id>/editar/  Editar
- /productos/<id>/eliminar/ Eliminar
- /categorias/           CRUD categorías
- /etiquetas/            CRUD etiquetas
- /admin/                Django Admin
- /accounts/login/       Login
- /accounts/logout/      Logout (POST; botón en la barra)

----------------------------------------------------------------
9) ESTRUCTURA CLAVE (RESUMEN)
----------------------------------------------------------------
config/                 (settings, urls)
inventario/             (models, forms, views, urls, admin)
templates/
  base.html
  index.html
  productos/ (lista.html, crear.html, editar.html, detalle.html, eliminar.html)
  categorias/ (lista.html, formulario.html, confirmar_eliminar.html)
  etiquetas/  (lista.html, formulario.html, confirmar_eliminar.html)
.env                   (local, PRIVADO)
.env.example           (plantilla de variables)
requirements.txt       (opcional)

----------------------------------------------------------------
10) MODELOS (RESUMEN)
----------------------------------------------------------------
Categoria(nombre, descripcion)
Etiqueta(nombre)
Producto(nombre, descripcion, precio, categoria FK, etiquetas M2M)
DetalleProducto(producto OneToOne, dimensiones, peso)

Relaciones:
- Categoria 1 --- N Producto
- Producto  M --- M Etiqueta
- Producto  1 --- 1 DetalleProducto

----------------------------------------------------------------
11) SEGURIDAD Y BUENAS PRÁCTICAS
----------------------------------------------------------------
- No subir .env ni credenciales (uso .gitignore).
- SECRET_KEY y DATABASE_URL siempre por variables de entorno.
- CSRF habilitado en todos los formularios con {% csrf_token %}.
- Autenticación requerida en CRUD (decorador @login_required).
- En producción: DEBUG=False, HTTPS activo, cookies seguras y HSTS (ver settings).
- Rotar contraseñas si temporalmente se activó "trust" en pg_hba.conf.
- Limitar usuarios del Admin y usar contraseñas únicas y robustas.

----------------------------------------------------------------
12) CONSULTAS ORM (EJEMPLOS)
----------------------------------------------------------------
Desde la shell:
(.venv) PS ...\inventario_django> python manage.py shell

from inventario.models import Producto, Categoria, Etiqueta
from django.db.models import Count, Avg, Min, Max

Producto.objects.filter(nombre__icontains="teclado")
Categoria.objects.annotate(total=Count("productos")).values("nombre","total")
Etiqueta.objects.get(nombre="gaming")
Producto.objects.raw("SELECT id, nombre, precio FROM inventario_producto ORDER BY precio DESC")

exit()

----------------------------------------------------------------
13) PROBLEMAS COMUNES (TROUBLESHOOTING)
----------------------------------------------------------------
• psql no reconocido:
  PS> Test-Path "C:\Program Files\PostgreSQL\17\bin"
  PS> $env:Path="$env:Path;C:\Program Files\PostgreSQL\17\bin"

• FATAL: autenticación password falló:
  - Revisa usuario/contraseña en .env (DATABASE_URL).
  - Confirma que el servicio "postgresql-x64-17" está RUNNING.
  - Revisa pg_hba.conf (uso de scram-sha-256 para ::1 y 127.0.0.1).

• Loop de login (next=/accounts/login/):
  - Base.html evita pasar next cuando request.path == "/accounts/login/".
  - LOGIN_REDIRECT_URL="/", LOGIN_URL="/accounts/login/".

----------------------------------------------------------------
14) CAPTURAS REQUERIDAS (para evaluación)
----------------------------------------------------------------
- Django Admin mostrando modelos (Productos/Categorías/Etiquetas/Detalle).
- Listado de Productos con acciones CRUD.
- Formularios de creación/edición.
- Página de detalle con etiquetas y detalle 1:1.
- Página de login y barra con Cerrar sesión.
