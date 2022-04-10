from django.urls import include, path
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

# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', include(router.urls)),

    path(r'artists/<int:pk>/records/', views.ArtistRecordViewSet.as_view({'get': 'list'})),
    path(r'artists/<int:pk>/songs/', views.ArtistSongViewSet.as_view({'get': 'list'})),
    path(r'artists/<int:pk>/comps/', views.ArtistCompsViewSet.as_view({'get': 'list'})),

    path(r'artists/<int:artist_id>/cover/', views.artist_cover),
    path(r'artists/<int:artist_id>/images/<int:image_id>/', views.artist_image_detail),

    path(r'records/<int:record_id>/cover/', views.record_cover),
    path(r'records/<int:record_id>/images/<int:image_id>/', views.record_image_detail),
]

# print('urlpatterns', urlpatterns)

# urlpatterns = format_suffix_patterns(urlpatterns)