# forums
Forums app for CSDT, based on Treehouse's MSG app developed by Kenneth Love for their Django Authentication tutorial, Logo and default avatar icons from [icons8](https://icons8.com/web-app/category/all/Messaging) and Theme from [Creative Tim](http://www.creative-tim.com/product/paper-kit).


# Please note:
Requires libffi-dev on server:
```
sudo apt-get install libffi-dev
```

It also requires Python 3.x.

Quick start
-----------
```
1. Add "forums" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bootstrap3',
        'accounts',
        'communities',
        'posts',
        
    ]

2. Include the forums URLconf in your project urls.py like this::

    
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r"^posts/", include("posts.urls", namespace="posts")),
    url(r"^communities/",
        include("communities.urls", namespace="communities")),


3. Run `python manage.py migrate` to create the forums models.
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
