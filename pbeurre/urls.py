"""pbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]"""

from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from aliments import views


urlpatterns = [
    url(r'^$', views.index,),
    url(r'^aliments/', include('aliments.urls')),
    url(r'^content/', admin.site.urls),
    url(r'^aliments/', include('django.contrib.auth.urls')),
    #url(r'^accounts/', include('aliments.urls')),
    path('accounts/profile/', include('aliments.urls', namespace='aliments')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
