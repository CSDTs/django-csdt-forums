# forums
Forums app for CSDT, based on Treehouse's MSG app developed by Kenneth Love for their Django Authentication tutorial.

Under /urls.py, add:
```python
url(r"^posts/", include("posts.urls", namespace="posts")),
url(r"^communities/", include("communities.urls", namespace="communities")),
```

