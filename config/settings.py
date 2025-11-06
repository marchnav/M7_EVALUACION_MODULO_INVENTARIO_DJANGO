"""
Django settings for config project.
Seguridad por defecto mediante variables de entorno (.env) y PostgreSQL vía DATABASE_URL.

Requiere:
  - django-environ
  - .env (local, privado) basado en .env.example
"""

from pathlib import Path
import environ

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------
# Entorno (.env)
# --------------------------------------------------------------------------------------
env = environ.Env()
# Carga el archivo .env (si existe). En producción se recomienda inyectar variables.
environ.Env.read_env(BASE_DIR / ".env")

# --------------------------------------------------------------------------------------
# Seguridad y modo
# --------------------------------------------------------------------------------------
# NUNCA hardcodear SECRET_KEY. Debe venir de .env
SECRET_KEY = env("SECRET_KEY")

# Debug desactivado por defecto si no se define (mejor práctica)
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://localhost", "http://127.0.0.1"],
)

# --------------------------------------------------------------------------------------
# Aplicaciones
# --------------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto
    "inventario",
]

# --------------------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# --------------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Habilita /templates a nivel proyecto
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------------------------------------------
# Base de datos (PostgreSQL por DATABASE_URL)
# Ejemplo en .env:
#   DATABASE_URL=postgres://usuario:password@localhost:5432/inventario
# --------------------------------------------------------------------------------------
DATABASES = {
    "default": env.db("DATABASE_URL")
}
# Mantener conexiones abiertas para mejorar rendimiento en dev/prod controlado
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DB_CONN_MAX_AGE", default=60)

# --------------------------------------------------------------------------------------
# Validación de contraseñas
# --------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------------------
# Internacionalización / Zona horaria Chile
# --------------------------------------------------------------------------------------
LANGUAGE_CODE = env("LANGUAGE_CODE", default="es-cl")
TIME_ZONE = env("TIME_ZONE", default="America/Santiago")
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------------------
# Archivos estáticos y media
# --------------------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # para collectstatic en despliegue
# Si más adelante agregas una carpeta /static para assets del proyecto:
# STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------------------------------------
# Config por defecto de PK
# --------------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------------------
# Autenticación (login/logout redirects)
# --------------------------------------------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# --------------------------------------------------------------------------------------
# Seguridad adicional (sólo se endurecen si DEBUG=False)
# --------------------------------------------------------------------------------------
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)  # ajusta en prod (ej. 31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=False)
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
    X_FRAME_OPTIONS = "DENY"
