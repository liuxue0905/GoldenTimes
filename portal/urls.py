from django.urls import include, path

from . import views
from portal.views import RecordListView, RecordDetailView
from portal.views import SongListView, SongDetailView
from portal.views import ArtistListView, ArtistDetailView
from portal.views import CompanyListView, CompanyDetailView
from portal.views import ArtistRecordList, ArtistSongList, ArtistRecordListInvolved
from portal.views import CompanyRecordListView

app_name = 'portal'
urlpatterns = [
    path("", views.index, name='index'),

    path("dashboard/", views.dashboard, name='dashboard'),

    path("about/", views.about, name='about'),

    path("records/", RecordListView.as_view(), name='record-list'),
    path("records/<int:pk>/", RecordDetailView.as_view(), name='record-detail'),

    path("songs/", SongListView.as_view(), name='song-list'),
    path("songs/<int:pk>/", SongDetailView.as_view(), name='song-detail'),

    path("artists/", ArtistListView.as_view(), name='artist-list'),
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name='artist-detail'),

    path("artists/<int:pk>/records/", ArtistRecordList.as_view(), name='artist-detail-record-list'),
    path("artists/<int:pk>/songs/", ArtistSongList.as_view(), name='artist-detail-song-list'),
    path("artists/<int:pk>/records/involved", ArtistRecordListInvolved.as_view(),
        name='artist-detail-record-list-involved'),

    path("companies/", CompanyListView.as_view(), name='company-list'),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name='company-detail'),
    path("companies/<int:pk>/records/", CompanyRecordListView.as_view(), name='company-record-list'),

    path("import/records/", views.LogImportRecordsView.as_view(), name='import-records'),
    path("import/artists/", views.LogImportArtistsView.as_view(), name='import-artists'),
]
