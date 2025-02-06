from .base import *

SECRET_KEY = "U6cfo0sw8kG13P_LykDnNdZC-896W9rJRA7AYYvxvPKkee4NFmMV_tW7BrYK1i23nyw"
ALLOWED_HOSTS = ["elkis.pythonanywhere.com"]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["https://elkis.pythonanywhere.com"]

X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
