"""GoldenTimes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls

from django.views.generic import RedirectView

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url='http://liujin.jios.org:8888')),
    path("", RedirectView.as_view(url='/portal/')),

    path("admin/", admin.site.urls),
    path("portal/", include('portal.urls')),

    path("api/", include('api.urls')),

    path("api-auth/", include('rest_framework.urls', namespace='rest_framework'))
]

# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
# # ... the rest of your URLconf here ...
#
# urlpatterns += staticfiles_urlpatterns()

urlpatterns = (
        [
            # ... the rest of your URLconf goes here ...
            *urlpatterns,
        ]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if not settings.TESTING:
    urlpatterns = [
                      *urlpatterns,
                  ] + debug_toolbar_urls()

if not settings.DEBUG:
    from .static_debug_false import static as static_debug_false
    urlpatterns = (
            [
                # ... the rest of your URLconf goes here ...
                *urlpatterns,
            ]
            + static_debug_false(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
            + static_debug_false(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
