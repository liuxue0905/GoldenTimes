from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

from portal.models import Artist, Record, Song
from .serializers import ArtistSerializer, RecordSerializer, SongSerializer

from portal.models import Company
from .serializers import CompanySerializer

from django.db.models import Q

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_queryset(self):
        queryset = Artist.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)

        record_isnull = self.request.query_params.get('record_isnull', None)
        print('record_isnull', record_isnull)
        if record_isnull is not None:
            record__isnull = record_isnull in ['true', '1']
            print('record__isnull', record__isnull)
            queryset = queryset.filter(record__isnull=record__isnull).distinct()

        return queryset


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_queryset(self):
        queryset = Record.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)
        format = self.request.query_params.get('format', None)
        if format is not None:
            queryset = queryset.filter(format=format)
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(year=year)
        company_id = self.request.query_params.get('company_id', None)
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)
        return queryset


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)
        return queryset


# class ArtistRecordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
class ArtistRecordViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_queryset(self):
        # print(self.lookup_url_kwarg)
        # print(self.kwargs)
        # print(self.request)
        # print(self.request.query_params)
        # print(self.request.data)

        pk = self.kwargs.get('pk')

        try:
            artist = Artist.objects.get(pk=pk)
        except Exception as e:
            print(e)
        else:
            # artist.record_set
            queryset = Record.objects.all()
            queryset = queryset.filter(artists__exact=artist)
            return queryset

            # return self.queryset.none()
        return Record.objects.none()


class ArtistSongViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Record.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        # print(self.lookup_url_kwarg)
        # print(self.kwargs)
        # print(self.request)
        # print(self.request.query_params)
        # print(self.request.data)

        pk = self.kwargs.get('pk')

        try:
            artist = Artist.objects.get(pk=pk)
        except Exception as e:
            print(e)
        else:
            # artist.song_set
            queryset = Song.objects.all()
            queryset = queryset.filter(artists__exact=artist)
            return queryset

        # return self.queryset.none()
        return Song.objects.none()


class ArtistRecord2ViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_queryset(self):
        # print(self.lookup_url_kwarg)
        # print(self.kwargs)
        # print(self.request)
        # print(self.request.query_params)
        # print(self.request.data)

        pk = self.kwargs.get('pk')

        try:
            artist = Artist.objects.get(pk=pk)
        except Exception as e:
            print(e)
        else:
            # artist.record_set
            queryset = Record.objects.all()
            queryset = queryset.filter(~Q(artists__exact=artist), song__artists__exact=artist).distinct()
            return queryset

        # return self.queryset.none()
        return Record.objects.none()
