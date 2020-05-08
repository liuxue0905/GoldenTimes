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

# router.register(r'artists/(?P<pk>[^/.]+)/records/', views.ArtistRecordViewSet)
# router.register(r'artists/(?P<pk>[^/.]+)/songs/', views.ArtistSongViewSet)
# router.register(r'artists/(?P<pk>[^/.]+)/comps/', views.ArtistCompsViewSet)

from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^artists/(?P<pk>[^/.]+)/records/$', views.ArtistRecordViewSet.as_view({'get': 'list'})),
    url(r'^artists/(?P<pk>[^/.]+)/songs/$', views.ArtistSongViewSet.as_view({'get': 'list'})),
    url(r'^artists/(?P<pk>[^/.]+)/comps/$', views.ArtistCompsViewSet.as_view({'get': 'list'})),

    url(r'^artists/(?P<artist_id>[^/.]+)/cover/$', views.artist_cover),
    # url(r'^artists/(?P<artist_id>[^/.]+)/images/$', views.artist_image_list),
    url(r'^artists/(?P<artist_id>[^/.]+)/images/(?P<image_id>[^/.]+)/$', views.artist_image_detail),

    url(r'^records/(?P<record_id>[^/.]+)/cover/$', views.record_cover),
    # url(r'^records/(?P<record_id>[^/.]+)/images/$', views.record_image_list),
    url(r'^records/(?P<record_id>[^/.]+)/images/(?P<image_id>[^/.]+)/$', views.record_image_detail),
]

# print('urlpatterns', urlpatterns)

# urlpatterns = format_suffix_patterns(urlpatterns)