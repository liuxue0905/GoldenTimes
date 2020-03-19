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
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include

from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'artists', views.ArtistViewSet)
router.register(r'records', views.RecordViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'companies', views.CompanyViewSet)
# router.register(r'artist-records', views.ArtistRecordViewSet)
# router.urls += url(r'^api/artists/(?P<pk>[^/.]+)/records/$', views.ArtistRecordViewSet.as_view({'get': 'list'})),

# print(router.urls)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^portal/', include('portal.urls')),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    ,
    url(r'^api/artists/(?P<pk>[^/.]+)/records/$', views.ArtistRecordViewSet.as_view({'get': 'list'})),
    url(r'^api/artists/(?P<pk>[^/.]+)/songs/$', views.ArtistSongViewSet.as_view({'get': 'list'})),
    url(r'^api/artists/(?P<pk>[^/.]+)/comps/$', views.ArtistRecord2ViewSet.as_view({'get': 'list'})),

]

# url(r'^api/artists/(?P<pk>[^/.]+)/compilation-records/$', views.ArtistRecord2ViewSet.as_view({'get': 'list'})),

# urlpatterns += url(r'^artists/{pk}/records/$', views.ArtistRecordViewSet.as_view())

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
