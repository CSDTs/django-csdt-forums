# forums
Forums app for CSDT, based on Treehouse's MSG app developed by Kenneth Love for their Django Authentication tutorial.

Required Apps:
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'django.contrib.humanize',
'bootstrap3',

Under /urls.py, add:
```python
url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r"^posts/", include("posts.urls", namespace="posts")),
    url(r"^communities/",
        include("communities.urls", namespace="communities")),
```

