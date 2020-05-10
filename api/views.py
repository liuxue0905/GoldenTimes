from django.core.files import File
from django.db.models.fields.files import ImageFieldFile
from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from imagekit.files import BaseIKFile
from pilkit.processors import Anchor
from pilkit.utils import FileWrapper
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

        _type = self.request.query_params.get('type', None)
        if _type is not None:
            queryset = queryset.filter(type=_type)

        type__isnull = self.request.query_params.get('type__isnull', None)
        print('type__isnull', type__isnull)
        if type__isnull is not None:
            type__isnull_value = type__isnull in ['true', '1']
            print('type__isnull_value', type__isnull_value)
            queryset = queryset.filter(type__isnull=type__isnull_value)

        record__isnull = self.request.query_params.get('record__isnull', None)
        if record__isnull is None:
            record__isnull = self.request.query_params.get('record_isnull', None)
        print('record__isnull', record__isnull)
        if record__isnull is not None:
            record__isnull_value = record__isnull in ['true', '1']
            print('record__isnull_value', record__isnull_value)
            queryset = queryset.filter(record__isnull=record__isnull_value).distinct()

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


from rest_framework.decorators import api_view
from django.http import HttpResponseNotFound
from django.http import FileResponse
from imagekit import ImageSpec
from imagekit.processors import ResizeToCover, ResizeToFit, Adjust, SmartResize, ResizeToFill, ResizeCanvas, Resize
from portal.imagekit.watermark import ImageWatermark
from imagekit.cachefiles import ImageCacheFile

from django.conf import settings
import os

from mimetypes import MimeTypes

mime_types = MimeTypes()


class GTImageSpec(ImageSpec):
    processors = [
        Resize(240, 240),

        # ResizeToFill(240, 240),

        # ResizeToCover(240, 240),

        # ResizeToFit(240, 240),
        # ResizeCanvas(240, 240, color='#000000', anchor=Anchor.CENTER),

        ImageWatermark(os.path.join(settings.MEDIA_ROOT, 'watermarks/watermark.png'),
                       position=('bottom', 'right'),
                       scale=True,
                       repeat=False,
                       opacity=0.8),
    ]
    format = 'JPEG'
    options = {'quality': 100}

    def __init__(self, source):
        super(GTImageSpec, self).__init__(source)
        self.source = source
        pass

    def config(self, resize, width, height):

        # print('config', 'resize', resize)
        # print('config', 'width', width)
        # print('config', 'height', height)

        self.processors = []

        if (width is not None) and (height is not None):
            if resize is None:
                self.processors.append(Resize(width, height))
            elif resize == 'cover':
                self.processors.append(ResizeToCover(width, height))
            elif resize == 'fill':
                self.processors.append(ResizeToFill(width, height))
            elif resize == 'fit':
                self.processors.append(ResizeToFit(width, height))
                self.processors.append(ResizeCanvas(width, height, color='#000000', anchor=Anchor.CENTER))

        self.processors.append(ImageWatermark(os.path.join(settings.MEDIA_ROOT, 'watermarks/watermark.png'),
                                              position=('bottom', 'right'),
                                              scale=True,
                                              repeat=False,
                                              opacity=0.8))

        self.format = 'JPEG'
        self.options = {'quality': 100}
        pass


# size width height resize=[None|cover|fill|fit] format=[JPEG] quality=[0-100]

def image_generate(request, image: ImageFieldFile):
    try:
        # print('cover', 'request.query_params', request.query_params)

        size = request.query_params.get('size', None)
        width = request.query_params.get('width', size)
        height = request.query_params.get('height', size)
        resize = request.query_params.get('resize', None)

        if size:
            size = int(size)
        if width:
            width = int(width)
        if height:
            height = int(height)

        # print('cover', type(size), size)
        # print('width', type(width), width)
        # print('height', type(height), height)
        # print('resize', resize)

        image_spec = GTImageSpec(source=image)
        image_spec.config(resize, width, height)
        return FileResponse(image_spec.generate(), content_type='image/jpeg')

        # cached = ImageCacheFile(image_spec)
        # cached.generate()
        # print('cached', type(cached), type(cached.file), cached, cached.file)
        # base_ik_file: BaseIKFile = cached
        # file: File = base_ik_file.file
        # return FileResponse(file.open(), content_type='image/jpeg')
    except Exception as e:
        print('cover', 'except', type(e), e, repr(e), e.__cause__)
        return HttpResponseNotFound()


@api_view(['GET'])
def artist_cover(request, artist_id):
    try:
        artist = Artist.objects.get(pk=artist_id)
        # print('artist', artist)
        # print('artist.artistavatar', artist.artistavatar)

        image = artist.artistavatar.image
        # return FileResponse(image.open(), content_type='image/jpeg')

        return image_generate(request, image)
    except Exception as e:
        print('artist_cover', 'except', e)
        return HttpResponseNotFound()


@api_view(['GET'])
def record_cover(request, record_id):
    try:
        record = Record.objects.get(pk=record_id)
        # print('record', record)
        # print('record.recordcover', record.recordcover)

        image = record.recordcover.image
        # return FileResponse(image.open(), content_type='image/jpeg')

        return image_generate(request, image)
    except Exception as e:
        print('record_cover', 'except', e)
        return HttpResponseNotFound()


@api_view(['GET'])
def artist_image_detail(request, artist_id, image_id):
    print('artist_image_detail', artist_id, image_id)

    try:
        artist = Artist.objects.get(pk=artist_id)
        image_model = artist.artistimages_set.get(pk=image_id)
        image = image_model.image

        return image_generate(request, image)
    except Exception as e:
        print('artist_image_detail', 'except', e)
        return HttpResponseNotFound()


@api_view(['GET'])
def record_image_detail(request, record_id, image_id):
    print('record_image_detail', record_id, image_id)

    try:
        record = Record.objects.get(pk=record_id)
        image_model = record.recordimages_set.get(pk=image_id)
        image = image_model.image

        return image_generate(request, image)
    except Exception as e:
        print('record_image_detail', 'except', e)
        return HttpResponseNotFound()
