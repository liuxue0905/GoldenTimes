# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
# from django.views import generic
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView

from portal.models import Record, Song, Artist, Company, ArtistImages, RecordImages


# Create your views here.


def index(request):
    # return HttpResponse("Hello, world. You're at the odm index.")

    # print(request)
    # print(type(request))
    # # < WSGIRequest: GET '/portal/' >
    # # < class 'django.core.handlers.wsgi.WSGIRequest'>
    # # import django.core.handlers.wsgi.WSGIRequest
    #
    # print('request.path', request.path)
    # print('request.body', request.body)
    # print('request.META', request.META)
    # print('request.COOKIES', request.COOKIES)
    #
    # print('request.META[\'HTTP_ACCEPT_LANGUAGE\']', request.META['HTTP_ACCEPT_LANGUAGE'])

    return HttpResponseRedirect(reverse('portal:dashboard', args=()))


def dashboard(request):
    queryset = Artist.objects.filter(record__isnull=False).distinct()

    # from collections import OrderedDict

    context = dict()

    object_list = list()
    object_list.append({'type': '男', 'artists': queryset.filter(type=1).all()})
    object_list.append({'type': '女', 'artists': queryset.filter(type=0).all()})
    object_list.append({'type': '组合', 'artists': queryset.filter(type=2).all()})
    object_list.append({'type': '其他', 'artists': queryset.filter(type__isnull=True).all()})

    context['object_list'] = object_list

    return render(request, 'portal/dashboard.html', context)


def about(request):
    return render(request, 'portal/about.html')


class RecordListView(ListView):
    model = Record
    # context_object_name = 'my_favorite_publishers'
    paginate_by = 20

    def get_queryset(self):
        title = self.request.GET.get('title')
        format = self.request.GET.get('format')

        queryset = Record.objects.all()

        if title:
            queryset = queryset.filter(title__contains=title)

        if format:
            queryset = queryset.filter(format=format)

        # from django.db.models import Prefetch
        # queryset = Record.objects.prefetch_related(Prefetch('song_set', queryset=Song.objects.order_by('track').all()))
        #
        # print(queryset[0].title)
        # print(queryset[0].song_set.all())

        return queryset


class RecordDetailView(DetailView):
    model = Record

    # context_object_name = 'my_favorite_publishers'

    def get_object(self, queryset=None):
        from django.db.models import Prefetch
        from django.db.models.functions import Cast
        from django.db.models import PositiveIntegerField

        obj: Record = super().get_object(queryset)

        # print('obj', obj)
        # print('obj.objects', obj.__class__.objects)
        # print('obj.song_set', obj.song_set)

        # print(obj.song_set.annotate(track_integer=Cast('track', PositiveIntegerField())).order_by('-track_integer'))
        # print(obj.song_set.annotate(track_integer=Cast('track', PositiveIntegerField())).order_by('-track_integer').count())

        # from django.db.models import OuterRef
        # print(Song.objects.filter(record=OuterRef('pk')).annotate(track_integer=Cast('track', PositiveIntegerField())).order_by('-track_integer'))

        # print(Song.objects.filter(record=obj).annotate(track_integer=Cast('track', PositiveIntegerField())).order_by('-track_integer'))

        prefetch = Prefetch('song_set', queryset=Song.objects.annotate(
            track_integer=Cast('track', PositiveIntegerField())).order_by('track_integer'))
        obj = Record.objects.filter(pk=obj.pk).prefetch_related(prefetch).get()

        return obj

    def get_context_data(self, **kwargs):
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        # record = Record.objects.get(pk=context['object'].id)
        # record.recordcover

        # from django.db.models.functions import Cast
        # from django.db.models import PositiveIntegerField
        # abc = record.song_set.annotate(track_integer=Cast('track', PositiveIntegerField())).order_by('-track_integer')
        #
        # print(abc)

        return context


class ArtistListView(ListView):
    model = Artist
    # context_object_name = 'my_favorite_publishers'
    paginate_by = 20

    def get_queryset(self):

        queryset = Artist.objects.all()

        def querystring_int(q):
            try:
                return int(q)
            except Exception as e:
                pass
                # print(e)
            return None

        def querystring_bool(q):
            if q in ['true', '1', 'True']:
                return True
            elif q in ['false', '0', 'False']:
                return False
            return None

        form_name = self.request.GET.get('name')
        form_type = querystring_int(self.request.GET.get('type'))
        form_record__isnull = querystring_bool(self.request.GET.get('record__isnull'))

        # print('form_record__isnull', form_record__isnull)

        if form_name is not None:
            queryset = queryset.filter(name__contains=form_name)

        if form_type is not None:
            queryset = queryset.filter(type=form_type)

        if form_record__isnull is not None:
            queryset = queryset.filter(record__isnull=form_record__isnull).distinct()

        # data = {
        #     'name': None,
        #     'type': None,
        #     'record__isnull': None
        # }
        # self.form = forms.ArtistListForm()

        # if self.form.is_valid():
        #     # print('get_queryset', 'form.data', self.form.data)
        #     # print('get_queryset', 'form.cleaned_data', self.form.cleaned_data)
        #     name = self.form.cleaned_data['name']
        #     type = self.form.cleaned_data['type']
        #     record__isnull = self.form.cleaned_data['record__isnull']
        #
        #     if name is not None:
        #         queryset = queryset.filter(name__contains=name)
        #
        #     if type is not None:
        #         queryset = queryset.filter(type=type)
        #
        #     if record__isnull is not None:
        #         queryset = queryset.filter(record__isnull=record__isnull).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # context['form'] = self.form
        # print('get_context_data', 'self.form', self.form)
        # print('get_context_data', 'self.form.data', self.form.data)
        # print('get_context_data', 'self.form.cleaned_data', self.form.cleaned_data)

        return context


class ArtistDetailView(DetailView):
    model = Artist

    # context_object_name = 'my_favorite_publishers'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        object = context['object']
        artist = object

        # Record Involved
        record_involved_set = Record.objects.filter(~Q(artists__exact=artist), song__artists__exact=artist)
        setattr(object, 'record_involved_set', record_involved_set)

        return context


class SongListView(ListView):
    model = Song
    # context_object_name = 'my_favorite_publishers'
    paginate_by = 20

    def get_queryset(self):
        title = self.request.GET.get('title')
        worker_type_1_name = self.request.GET.get('worker_type_1')
        worker_type_2_name = self.request.GET.get('worker_type_2')

        queryset = Song.objects.order_by('title').all()

        if title:
            queryset = queryset.filter(title__contains=title)

        if worker_type_1_name:
            queryset = queryset.filter(songworker__type_id=1, songworker__name__contains=worker_type_1_name)
        if worker_type_2_name:
            queryset = queryset.filter(songworker__type_id=2, songworker__name__contains=worker_type_2_name)

        return queryset


class SongDetailView(DetailView):
    model = Song

    # context_object_name = 'my_favorite_publishers'

    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CompanyListView(ListView):
    model = Company
    # context_object_name = 'my_favorite_publishers'
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name')
        order_by = self.request.GET.get('orderby')
        return Company.objects.filter(name__contains=name)
        # return Company.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompanyListView, self).get_context_data(**kwargs)
        # Add in the publisher
        # context['name'] = self.name
        # context['order_by'] = self.order_by
        return context


class CompanyDetailView(DetailView):
    model = Company

    # context_object_name = 'my_favorite_publishers'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        return context


def get_participated_album(artist):
    records = Record.objects.filter(~Q(artists__exact=artist), song__artists__exact=artist).distinct()
    return records


class ArtistRecordList(ListView):
    model = Record
    template_name = 'portal/artist_detail_record_list.html'
    # context_object_name = ''
    paginate_by = 20

    def get_queryset(self):
        queryset = super(ArtistRecordList, self).get_queryset()

        pk = self.kwargs['pk']
        self.artist = get_object_or_404(Artist, pk=pk)

        # Record.objects.filter(artists__exact=self.artist)

        queryset = queryset.filter(artists__exact=self.artist)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArtistRecordList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        context['object'] = self.artist

        # Record Involved
        # record_involved_set = Record.objects.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)
        # setattr(self.artist, 'record_involved_set', record_involved_set)

        setattr(self.artist, 'record_involved_set', get_participated_album(self.artist))

        return context


class ArtistSongList(ListView):
    model = Song
    template_name = 'portal/artist_detail_song_list.html'
    # context_object_name = ''
    paginate_by = 20

    def get_queryset(self):
        queryset = super(ArtistSongList, self).get_queryset()

        pk = self.kwargs['pk']
        self.artist = get_object_or_404(Artist, pk=pk)

        # Record.objects.filter(artists__exact=self.artist)

        queryset = queryset.filter(artists__exact=self.artist)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArtistSongList, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        context['object'] = self.artist

        # Record Involved
        # record_involved_set = Record.objects.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)
        # setattr(self.artist, 'record_involved_set', record_involved_set)

        setattr(self.artist, 'record_involved_set', get_participated_album(self.artist))

        return context


class ArtistRecordListInvolved(ListView):
    model = Record
    template_name = 'portal/artist_detail_record_list_involved.html'
    # context_object_name = ''
    paginate_by = 20

    def get_queryset(self):
        queryset = super(ArtistRecordListInvolved, self).get_queryset()

        pk = self.kwargs['pk']
        self.artist = get_object_or_404(Artist, pk=pk)

        # Record.objects.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)

        # queryset = queryset.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)
        #
        # # Record Involved
        # record_involved_set = Record.objects.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)

        queryset = queryset.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist).distinct()

        # Record Involved
        record_involved_set = queryset
        setattr(self.artist, 'record_involved_set', record_involved_set)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArtistRecordListInvolved, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        context['object'] = self.artist

        return context


class CompanyRecordListView(ListView):
    model = Record
    template_name = 'portal/company_record_list.html'
    # context_object_name = 'my_favorite_publishers'
    paginate_by = 20

    def get_queryset(self):
        queryset = super(CompanyRecordListView, self).get_queryset()

        pk = self.kwargs['pk']
        self.company = get_object_or_404(Company, pk=pk)

        queryset = queryset.filter(company=self.company)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CompanyRecordListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        context['object'] = self.company

        return context


#

def handle_uploaded_file_import_records(f):
    # import django.core.files.uploadhandler.InMemoryUploadedFile

    import os
    from datetime import datetime

    print('handle_uploaded_file', type(f), f)
    print('handle_uploaded_file', f)
    print('handle_uploaded_file', f.file)
    print('handle_uploaded_file', f.name)

    # print('handle_uploaded_file', 'f.temporary_file_path()', f.temporary_file_path())

    def make_filename(datetime_now):
        dir_excel = os.path.join(os.path.join(os.path.abspath(settings.MEDIA_ROOT), 'import/record'),
                                 datetime_now.strftime("%Y-%m-%d"))
        if not os.path.exists(dir_excel):
            os.makedirs(dir_excel)

        return os.path.join(dir_excel, datetime_now.strftime("%Y%m%d.%H%M%S.%f") + '.csv')

    datetime_start = datetime.now()

    from django.conf import settings
    filename = make_filename(datetime_start)

    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    from portal.parser.record import RecordParser
    parser = RecordParser(filename)

    import threading
    thread = threading.Thread(target=(lambda: parser.parse_with_db()))
    thread.daemon = True
    thread.start()


def handle_uploaded_file_import_artists(f):
    # import django.core.files.uploadhandler.InMemoryUploadedFile

    import os
    from datetime import datetime

    print('handle_uploaded_file', type(f), f)
    print('handle_uploaded_file', f)
    print('handle_uploaded_file', f.file)
    print('handle_uploaded_file', f.name)

    # print('handle_uploaded_file', 'f.temporary_file_path()', f.temporary_file_path())

    def make_filename(datetime_now):
        dir_excel = os.path.join(os.path.join(os.path.abspath(settings.MEDIA_ROOT), 'import/artist'),
                                 datetime_now.strftime("%Y-%m-%d"))
        if not os.path.exists(dir_excel):
            os.makedirs(dir_excel)

        return os.path.join(dir_excel, datetime_now.strftime("%Y%m%d.%H%M%S.%f") + '.csv')

    datetime_start = datetime.now()

    from django.conf import settings
    filename = make_filename(datetime_start)

    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    from portal.parser.artist import ArtistParser
    parser = ArtistParser(filename)

    import threading
    thread = threading.Thread(target=(lambda: parser.parse_with_db()))
    thread.daemon = True
    thread.start()


# class FileFieldView(LoginRequiredMixin, FormView, ListView):
class LogImportRecordsView(LoginRequiredMixin, FormView, ListView):
    from portal.forms import ExcelForms

    login_url = '/admin/login/'
    redirect_field_name = 'next'

    form_class = ExcelForms
    template_name = 'portal/import-records.html'  # Replace with your template.
    success_url = '/portal/import/records/'  # Replace with your URL or reverse().

    # success_url = reverse('portal:excel', args=())  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # files = request.FILES.getlist('file')
        file = request.FILES['file']
        print('file', file)
        if form.is_valid():
            # for f in files:
            #     # Do something with each file.
            handle_uploaded_file_import_records(request.FILES['file'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    paginate_by = 10

    def get_queryset(self):
        from portal.models import LogImportRecord
        queryset = LogImportRecord.objects.all()

        # print('FileFieldView', 'queryset', queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LogImportRecordsView, self).get_context_data(**kwargs)

        # context['status'] = ExcelLog.STATUS_CHOICES

        return context


# class FileFieldView(LoginRequiredMixin, FormView, ListView):
class LogImportArtistsView(LoginRequiredMixin, FormView, ListView):
    from portal.forms import ExcelForms

    login_url = '/admin/login/'
    redirect_field_name = 'next'

    form_class = ExcelForms
    template_name = 'portal/import-artists.html'  # Replace with your template.
    success_url = '/portal/import/artists/'  # Replace with your URL or reverse().

    # success_url = reverse('portal:excel', args=())  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # files = request.FILES.getlist('file')
        file = request.FILES['file']
        print('file', file)
        if form.is_valid():
            # for f in files:
            #     # Do something with each file.
            handle_uploaded_file_import_records(request.FILES['file'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    paginate_by = 10

    def get_queryset(self):
        from portal.models import LogImportArtist
        queryset = LogImportArtist.objects.all()

        # print('FileFieldView', 'queryset', queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LogImportArtistsView, self).get_context_data(**kwargs)

        # context['status'] = ExcelLog.STATUS_CHOICES

        return context


from django.http import HttpRequest
from django.http import HttpResponseNotFound
from GoldenTimes import settings
import os
from PIL import Image
from io import BytesIO

def record_cover(request: HttpRequest, pk, id: str, size: str):
    # print("record_cover", "pk", pk)
    # print("record_cover", "id", id)
    # print("record_cover", "size", size)

    try:
        id_str = id

        # path_image = ""
        if id_str == 'front':
            record = Record.objects.get(pk=pk)
            path_image = record.recordcover.image.path
        else:
            object = RecordImages.objects.get(pk=id_str)
            path_image = object.image.path
        #     print('object', object)
        # print('path_image', path_image)

        size_str = size

        # 支持的尺寸
        VALID_SIZES = [250, 500, 1200]
        default_size = 250
        # size_param = request.GET.get('size', str(default_size))
        if size_str == 'small':
            size = 250
        elif size_str == 'large':
            size = 500
        else:
            try:
                size = int(size_str)
                if size not in VALID_SIZES:
                    size = default_size  # 如果不在支持的尺寸中，用默认值
            except ValueError:
                size = default_size
            # print("size", size)

        image = thumbnail(path_image, size)

        # 保存到内存并返回
        buffer = BytesIO()
        image.convert('RGB').save(buffer, format="JPEG")  # 转为 RGB 保存为 JPG
        buffer.seek(0)

        # 返回图片响应
        return HttpResponse(buffer.getvalue(), content_type="image/jpeg")
    # except Exception as e:
        # print('record_cover', 'except', e)
        # return HttpResponseNotFound(e)
    except:
        return HttpResponseNotFound()

    # try:
    #     pass
    # except Exception as e:
    #     return HttpResponseBadRequest(f"Error processing image: {str(e)}")

def artist_cover(request: HttpRequest, pk, id: str, size: str):
    # print("record_cover", "pk", pk)
    # print("record_cover", "id", id)
    # print("record_cover", "size", size)

    try:

        id_str = id

        path_image = ""
        if id_str == 'avatar':
            artist = Artist.objects.get(pk=pk)
            path_image = artist.artistavatar.image.path
        else:
            object = ArtistImages.objects.get(pk=id_str)
            path_image = object.image.path
        # print('path_image', path_image)

        size_str = size

        # 支持的尺寸
        VALID_SIZES = [36, 48, 64, 128, 144, 250, 500, 1200]
        default_size = 250
        # size_param = request.GET.get('size', str(default_size))
        if size_str == 'small':
            size = 250
        elif size_str == 'large':
            size = 500
        else:
            try:
                size = int(size_str)
                if size not in VALID_SIZES:
                    size = default_size  # 如果不在支持的尺寸中，用默认值
            except ValueError:
                size = default_size
            # print("size", size)

        image = thumbnail(path_image, size)

        # 保存到内存并返回
        buffer = BytesIO()
        image.convert('RGB').save(buffer, format="JPEG")  # 转为 RGB 保存为 JPG
        buffer.seek(0)

        # 返回图片响应
        return HttpResponse(buffer.getvalue(), content_type="image/jpeg")
    # except Exception as e:
    # print('record_cover', 'except', e)
    # return HttpResponseNotFound(e)
    except Exception as e:
    # except:
        print(__name__, 'except', e)
        return HttpResponseNotFound()

def thumbnail(path, size) -> Image:
    path_watermark = os.path.join(settings.MEDIA_ROOT, 'watermarks','watermark.png')

    image = Image.open(path).convert('RGBA')
    watermark = Image.open(path_watermark).convert('RGBA')

    image.thumbnail((size, size), Image.Resampling.LANCZOS)

    # # 水印缩放（假设水印占图片宽度的 1/4）
    # watermark_ratio = new_width / original_width / 4  # 水印按比例缩放
    watermark_ratio = min(image.width / watermark.width, image.height / watermark.height)
    # print("watermark_ratio", watermark_ratio)
    resize_size = (int(watermark.size[0] * watermark_ratio), int(watermark.size[1] * watermark_ratio))
    watermark = watermark.resize(resize_size, Image.Resampling.LANCZOS)

    # print("image.size", image.size)
    # print("watermark.size", watermark.size)

    image.paste(watermark, (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1]), watermark)

    return image
