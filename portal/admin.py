# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.


from .models import Record, Song, Artist, Company, RecordCover, RecordImages, ArtistAvatar, ArtistImages, ExcelLog


# admin.StackedInline
# admin.TabularInline
class SongAdmin(admin.StackedInline):
    # class SongAdmin(admin.TabularInline):
    model = Song
    extra = 0
    filter_horizontal = ('artists',)


class RecordCoverAdmin(admin.StackedInline):
# class RecordCoverAdmin(admin.TabularInline):
    model = RecordCover
    fields = ('image',)


# class RecordImagesAdmin(admin.StackedInline):
class RecordImagesAdmin(admin.TabularInline):
    model = RecordImages
    extra = 0
    fields = ('image',)


class RecordAdmin(admin.ModelAdmin):
    model = Record

    filter_horizontal = ('artists',)
    inlines = [SongAdmin, RecordCoverAdmin, RecordImagesAdmin]

    # list_display = ('cover', 'title', 'artist_list', 'release', 'number', 'format', 'company')
    list_display = ('title', 'artist_list', 'release', 'number', 'format', 'company')
    list_display_links = ('title', 'number',)
    list_filter = ('format',)
    list_per_page = 100
    list_select_related = ('company',)

    search_fields = ('title', 'number',)

    # ordering = ('title', 'release')

    def cover(self, object):
        return '<img src="{src}" width="13" height="13">'.format(src=object.recordcover.image.url)

    cover.allow_tags = True
    cover.short_description = ''

    def artist_list(self, object):
        artist_list = ''
        for index, artist in enumerate(object.artists.all()):
            if index != 0:
                # artist_list += '&nbsp;'
                artist_list += '/'
            artist_list += '<a href="/admin/portal/artist/{id}">{name}</a>'.format(id=artist.id, name=artist.name)
        return artist_list

    artist_list.allow_tags = True
    artist_list.short_description = '歌手'


class ArtistAvatarAdmin(admin.StackedInline):
# class ArtistAvatarAdmin(admin.TabularInline):
    model = ArtistAvatar
    fields = ('image',)


# class ArtistImagesAdmin(admin.StackedInline):
class ArtistImagesAdmin(admin.TabularInline):
    model = ArtistImages
    extra = 0
    fields = ('image',)


class ArtistAdmin(admin.ModelAdmin):
    model = Artist

    inlines = [ArtistAvatarAdmin, ArtistImagesAdmin]

    # list_display = ('avatar', 'name', 'type')
    list_display = ('name', 'type')
    list_display_links = ('name',)
    list_filter = ('type',)
    list_per_page = 100

    search_fields = ('name',)

    def avatar(self, object):
        return '<img src="{src}" width="13" height="13">'.format(src=object.artistavatar.image.url)

    avatar.allow_tags = True
    avatar.short_description = ''


class CompanyAdmin(admin.ModelAdmin):
    model = Company

    list_display = ('name',)
    list_filter = ('name',)
    list_per_page = 100

    search_fields = ('name',)


class ExcelLogAdmin(admin.ModelAdmin):
    module = ExcelLog

    list_display = ('datetime_start', 'file_excel_filename', 'file_log_filename', 'status', 'created_at')
    # list_display_links = ('file_excel_filename', 'file_log_filename',)
    # list_filter = ('name',)
    list_per_page = 100

    # search_fields = ('name',)

    def file_excel_filename(self, object):
        import os
        return os.path.basename(object.file_excel.name)

    def file_log_filename(self, object):
        import os
        return os.path.basename(object.file_log.name)


admin.site.register(Record, RecordAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(ExcelLog, ExcelLogAdmin)
