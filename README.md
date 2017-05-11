# forums
Forums app for CSDT, based on Treehouse's MSG app developed by Kenneth Love for their Django Authentication tutorial.
```
cffi==1.7.0
Django==1.9.9
django-allauth
django-analytical
django-attachments

django-bootstrap3
django-braces
django_compressor
django-extra-views
django-sekizai
django-taggit
django-taggit-templatetags2
misaka
pillow
psycopg2
pycparser
python-resize-image
sorl-thumbnail
sqlparse
twitter-text-python
```

Under /urls.py, add:
```python
url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r"^posts/", include("posts.urls", namespace="posts")),
    url(r"^communities/",
        include("communities.urls", namespace="communities")),
```

I have this as the settings.py addendum, will have to change depending on your setup:
```
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets'),]
STATIC_ROOT = '/static/'

LOGIN_REDIRECT_URL = "posts:all"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

AUTH_USER_MODEL = "accounts.User"

SITE_ID = 1

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

USER_IMAGE_PATH = '/assets/user_data/'


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
```
