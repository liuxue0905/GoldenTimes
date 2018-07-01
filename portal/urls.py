from django.conf.urls import url

from . import views
from portal.views import RecordListView, RecordDetailView
from portal.views import SongListView, SongDetailView
from portal.views import ArtistListView, ArtistDetailView
from portal.views import CompanyListView, CompanyDetailView
from portal.views import ArtistRecordList, ArtistSongList, ArtistRecordListInvolved
from portal.views import CompanyRecordListView

app_name = 'portal'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^about/$', views.about, name='about'),

    url(r'^records/$', RecordListView.as_view(), name='record-list'),
    url(r'^records/(?P<pk>[0-9]+)/$', RecordDetailView.as_view(), name='record-detail'),

    url(r'^songs/$', SongListView.as_view(), name='song-list'),
    url(r'^songs/(?P<pk>[0-9]+)/$', SongDetailView.as_view(), name='song-detail'),

    url(r'^artists/$', ArtistListView.as_view(), name='artist-list'),
    url(r'^artists/(?P<pk>[0-9]+)/$', ArtistDetailView.as_view(), name='artist-detail'),

    url(r'^artists/(?P<pk>[0-9]+)/records/$', ArtistRecordList.as_view(), name='artist-detail-record-list'),
    url(r'^artists/(?P<pk>[0-9]+)/songs/$', ArtistSongList.as_view(), name='artist-detail-song-list'),
    url(r'^artists/(?P<pk>[0-9]+)/records/involved$', ArtistRecordListInvolved.as_view(),
        name='artist-detail-record-list-involved'),

    url(r'^companies/$', CompanyListView.as_view(), name='company-list'),
    url(r'^companies/(?P<pk>[0-9]+)/$', CompanyDetailView.as_view(), name='company-detail'),
    url(r'^companies/(?P<pk>[0-9]+)/records/$', CompanyRecordListView.as_view(), name='company-record-list'),

    url(r'^import/records/$', views.LogImportRecordsView.as_view(), name='import-records'),
    url(r'^import/artists/$', views.LogImportArtistsView.as_view(), name='import-artists'),
]
