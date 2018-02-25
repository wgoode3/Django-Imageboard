# Setting up file uploads...

### add to ```settings.py```

```python
TEMPLATES[0]["OPTIONS"]["context_processors"].append('django.template.context_processors.media')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### add to ```urls.py```

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # your paths...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### in ```index.html```

In the form with an ```<input type="file">``` don't forget to include ```enctype="multipart/form-data"``` in the ```<form>``` tag.


Display the image with ```<img src="{{ MEDIA_URL }}{{ file.image }}" alt="img">```.
