from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'artists', views.ArtistViewSet)
router.register(r'records', views.RecordViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'companies', views.CompanyViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^artists/(?P<pk>[^/.]+)/records/$', views.ArtistRecordViewSet.as_view({'get': 'list'})),
    url(r'^artists/(?P<pk>[^/.]+)/songs/$', views.ArtistSongViewSet.as_view({'get': 'list'})),
    url(r'^artists/(?P<pk>[^/.]+)/comps/$', views.ArtistCompsViewSet.as_view({'get': 'list'})),
]
