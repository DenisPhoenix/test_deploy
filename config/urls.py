"""
    1. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
