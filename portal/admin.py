# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill, ResizeToCover
from imagekit.cachefiles import ImageCacheFile


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(17, 17)]
    format = 'JPEG'
    options = {'quality': 60}


def cached_admin_thumb_record_recordcover(instance):
    try:
        # `image` is the name of the image field on the model
        cached = ImageCacheFile(AdminThumbnailSpec(instance.recordcover.image))
        # only generates the first time, subsequent calls use cache
        cached.generate()
        return cached
    except Exception as e:
        print(e)
    return None


def cached_admin_thumb_artist(instance):
    try:
        # `image` is the name of the image field on the model
        cached = ImageCacheFile(AdminThumbnailSpec(instance.artistavatar.image))
        # only generates the first time, subsequent calls use cache
        cached.generate()
        return cached
    except Exception as e:
        print(e)
    return None


# Register your models here.


from .models import Record, Song, Artist, Company, RecordCover, RecordImages, ArtistAvatar, ArtistImages
from .models import WorkType, Work, LRecordWork, LSongWork
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


# class LRecordWorkAdmin(admin.TabularInline):
#     model = LRecordWork
#     extra = 0
#
#     fields = ('work',)


class RecordAdmin(admin.ModelAdmin):
    model = Record

    filter_horizontal = ('artists',)
    inlines = [SongAdmin, RecordCoverAdmin, RecordImagesAdmin]

    list_display = (
        'cover', 'title', 'number', 'artist_list', 'year', 'release_detail', 'release_order', 'format', 'company',
    )
    list_display_links = ('title', 'number',)
    list_filter = ('format',)
    list_per_page = 100
    list_select_related = ('company',)

    search_fields = ('title', 'number',)

    # ordering = ('title', 'release')

    cover = AdminThumbnail(image_field=cached_admin_thumb_record_recordcover)
    cover.short_description = ''

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
    list_display = ('cover', 'name', 'type')
    list_display_links = ('name',)
    list_filter = ('type',)
    list_per_page = 100

    search_fields = ('name',)

    cover = AdminThumbnail(image_field=cached_admin_thumb_artist)
    cover.short_description = ''

    # def avatar(self, object):
    #     return '<img src="{src}" width="13" height="13">'.format(src=object.artistavatar.image.url)
    #
    # avatar.allow_tags = True
    # avatar.short_description = ''


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


class WorkTypeAdmin(admin.ModelAdmin):
    module = WorkType
    list_display = ('name', 'description')
    list_per_page = 100


admin.site.register(Record, RecordAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Company, CompanyAdmin)

admin.site.register(WorkType, WorkTypeAdmin)

admin.site.register(LogImportRecord, LogImportRecordAdmin)
admin.site.register(LogImportArtist, LogImportArtistAdmin)
