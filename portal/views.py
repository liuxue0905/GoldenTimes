# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from portal.models import Record, Song, Artist, Company

import portal.forms as forms

from django.views.generic import ListView, DetailView, FormView
# from django.views import generic
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


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

        data = {
            'name': self.request.GET.get('name'),
            'type': self.request.GET.get('type'),
            'has_records': self.request.GET.get('has_records', True)
        }
        self.form = forms.ArtistListForm(data)
        # print('get_queryset', 'form', self.form, self.form.as_table())
        # print('get_queryset', 'form.is_valid()', self.form.is_valid())
        # print('get_queryset', 'form.errors', self.form.errors)

        if self.form.is_valid():
            # print('get_queryset', 'form.data', self.form.data)
            # print('get_queryset', 'form.cleaned_data', self.form.cleaned_data)
            name = self.form.cleaned_data['name']
            type = self.form.cleaned_data['type']
            has_records = self.form.cleaned_data['has_records']

            if name is not None:
                queryset = queryset.filter(name__contains=name)

            if type is not None:
                queryset = queryset.filter(type=type)

            if has_records:
                queryset = queryset.filter(record__isnull=False).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        context['form'] = self.form
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
    paginate_by = 100

    def get_queryset(self):
        title = self.request.GET.get('title')

        queryset = Song.objects.order_by('title').all()

        if title:
            queryset = queryset.filter(title__contains=title)

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
        record_involved_set = Record.objects.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)
        setattr(self.artist, 'record_involved_set', record_involved_set)

        return context


class ArtistSongList(ListView):
    model = Song
    template_name = 'portal/artist_detail_song_list.html'
    # context_object_name = ''
    paginate_by = 10

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
        record_involved_set = Record.objects.filter(~Q(artists__exact=self.artist), song__artists__exact=self.artist)
        setattr(self.artist, 'record_involved_set', record_involved_set)

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
    paginate_by = 10

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
