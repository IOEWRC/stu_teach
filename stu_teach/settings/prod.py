from stu_teach.settings.base import *
import dj_database_url
from decouple import config


DEBUG = False
ALLOWED_HOSTS = ['*']


# CORS_REPLACE_HTTPS_REFERER = True
# HOST_SCHEME = "https://"
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 1000000
# SECURE_FRAME_DENY = True

# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL')
#     )
# }

DATABASES = {
      'default': dj_database_url.config(
          default='sqlite:////{0}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
      )
  }


EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')

#for hosting media files
# Do not change any of these names
B2_BUCKET_NAME = config('HB2_B2_BUCKET_NAME')
B2_BUCKET_ID = config('HB2_B2_BUCKET_ID')
B2_ACCOUNT_ID = config('HB2_B2_ACCOUNT_ID')
B2_APPLICATION_KEY = config('HB2_B2_APP_KEY')
DEFAULT_FILE_STORAGE = 'django_b2storage.backblaze_b2.B2Storage'


