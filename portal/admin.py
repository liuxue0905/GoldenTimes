# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from imagekit.admin import AdminThumbnail


# Register your models here.


from .models import Record, Song, Artist, Company, RecordCover, RecordImages, ArtistAvatar, ArtistImages
from .models import LogImportRecord, LogImportArtist


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
    list_display = ('title', 'number', 'artist_list', 'release', 'format', 'company')
    list_display_links = ('title', 'number',)
    list_filter = ('format',)
    list_per_page = 100
    list_select_related = ('company',)

    search_fields = ('title', 'number',)

    # ordering = ('title', 'release')

    def artist_list(self, object):
        from django.utils.html import format_html_join
        from django.utils.safestring import mark_safe

        # # assuming get_full_address() returns a list of strings
        # # for each line of the address and you want to separate each
        # # line by a linebreak
        # return format_html_join(
        #     mark_safe('<br/>'),
        #     '{}',
        #     ((line,) for line in instance.get_full_address()),
        # ) or mark_safe("<span class='errors'>I can't determine this address.</span>")

        return format_html_join(
            mark_safe('<br/>'),
            '<a href="/admin/portal/artist/{}">{}</a>',
            ((artist.id, artist.name) for artist in object.artists.all()),
        ) or mark_safe("<span class='errors'></span>")

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


class LogImportRecordAdmin(admin.ModelAdmin):
    module = LogImportRecord

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


class LogImportArtistAdmin(admin.ModelAdmin):
    module = LogImportArtist

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
admin.site.register(LogImportRecord, LogImportRecordAdmin)
admin.site.register(LogImportArtist, LogImportArtistAdmin)
