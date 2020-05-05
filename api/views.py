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

# from rest_framework import generics
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from rest_framework.pagination import PageNumberPagination
# from rest_framework import mixins

from rest_framework.decorators import action


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
        print('name', name)
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

    # def get_object(self):
    #     object: Artist = super().get_object()
    #
    #     object.__setattr__('comp_set', self.get_comps_queryset())
    #
    #     return object
    #
    # def get_comps_queryset(self):
    #     pk = self.kwargs.get('pk')
    #
    #     try:
    #         artist = Artist.objects.get(pk=pk)
    #     except Exception as e:
    #         print(e)
    #     else:
    #         # artist.record_set
    #         queryset = Record.objects.all()
    #         queryset = queryset.filter(~Q(artists__exact=artist), song__artists__exact=artist).distinct()
    #         return queryset
    #
    #     # return self.queryset.none()
    #     return Record.objects.none()


class RecordViewSet(viewsets.ReadOnlyModelViewSet):
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
        queryset = self.queryset
        # queryset = Company.objects.all()
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


class ArtistCompsViewSet(viewsets.ReadOnlyModelViewSet):
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


from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import FileResponse
from django.http import Http404

from mimetypes import MimeTypes
mime_types = MimeTypes()


@api_view(['GET'])
def artist_cover(request, artist_id):
    print('artist_cover', artist_id)
    try:
        artist = Artist.objects.get(pk=artist_id)
        print('artist', artist)
        print('artist.artistavatar', artist.artistavatar)

        image = artist.artistavatar.image

        (type, encoding) = mime_types.guess_type(image.name)
        print('type', type)
        print('encoding', encoding)

        return FileResponse(image.open(), content_type=type)

    except Exception as e:
        print('artist_cover', 'except', e)
        pass
        # return Http404()
        return HttpResponseNotFound()


@api_view(['GET'])
def record_cover(request, record_id):
    print('record_cover', record_id)
    try:
        record = Record.objects.get(pk=record_id)
        print('record', record)
        print('record.recordcover', record.recordcover)

        image = record.recordcover.image

        (type, encoding) = mime_types.guess_type(image.name)
        print('type', type)
        print('encoding', encoding)

        return FileResponse(image.open(), content_type=type)
    except Exception as e:
        print('record_cover', 'except', e)
        pass
        # return Http404()
        return HttpResponseNotFound()


@api_view(['GET'])
def artist_image_list(request, artist_id):
    print('artist_image_list', artist_id)

    try:
        artist = Artist.objects.get(pk=artist_id)
        print('artist', artist)
        print('artist.artistavatar', artist.artistavatar)
        print('artist.artistimages_set', artist.artistimages_set)
        print('artist.artistimages_set.count()', artist.artistimages_set.count())
    except Exception as e:
        print('except', e)
        pass
    return Response({'key1': 'value1'})


@api_view(['GET'])
def artist_image_detail(request, artist_id, image_id):
    print('artist_image_list', artist_id, image_id)
    return Response({'key1': 'value1'})


@api_view(['GET'])
def record_image_list(request, record_id):
    print('record_image_list', record_id)

    try:
        record = Record.objects.get(pk=record_id)
        print('record', record)
        print('record.recordcover', record.recordcover)
        print('record.recordimages_set', record.recordimages_set)
        print('record.recordimages_set.count()', record.recordimages_set.count())
        print('record.recordimages_set.all()', record.recordimages_set.all())

        # record.recordimages_set.all()
        # from django.db.models import QuerySet
        # qs : QuerySet

        for image in record.recordimages_set.all():
            print('image', image)
            print('image', image.id, image.image, image.width, image.height)
            print('image.image', image.image.name, image.image.path, image.image.width, image.image.height)

            from mimetypes import MimeTypes
            mime_types = MimeTypes()

            (type, encoding) = mime_types.guess_type(image.image.name)
            print('type', type)
            print('encoding', encoding)

    except Exception as e:
        print('except', e)
        pass

    return Response({'key1': 'value1'})


@api_view(['GET'])
def record_image_detail(request, record_id, image_id):
    print('record_image_detail', record_id, image_id)
    print('record_image_detail', 'request.path', request.path)
    print('record_image_detail', 'request.query_params', request.query_params)

    return Response({'key1': 'value1'})
