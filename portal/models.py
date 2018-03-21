# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import os

# from django.core.files.storage import default_storage

from django.core.files.storage import FileSystemStorage


# FileStorage get_valid_name [ECHO]_[PA-FPD 001].jpg
# FileStorage get_available_name record/[ECHO]_[PA-FPD 001]/ECHO_PA-FPD_001.jpg 100

# FileStorage get_valid_name name [ECHO][PA-FPD 001].jpg
# FileStorage get_valid_name ret ECHOPA-FPD_001.jpg
# FileStorage get_available_name record/[ECHO][PA-FPD 001]/ECHOPA-FPD_001.jpg 100
# FileStorage get_available_name ret record/[ECHO][PA-FPD 001]/ECHOPA-FPD_001.jpg


class FileStorage(FileSystemStorage):
    def generate_filename(self, filename):
        self.filename = filename
        print('filename', filename)
        return super().generate_filename(filename)

    def get_valid_name(self, name):
        print('FileStorage', 'get_valid_name', 'name', name)

        ret = super().get_valid_name(name)
        print('FileStorage', 'get_valid_name', 'super().get_valid_name(name)', ret)

        import portal.util as util
        name = util.lx_quote(name)
        print('FileStorage', 'get_valid_name', 'name2', name)
        return name

    # def get_available_name(self, name, max_length=None):
    #     print('FileStorage', 'get_available_name', name, max_length)
    #     ret = super().get_available_name(name, max_length)
    #     print('FileStorage', 'get_available_name', 'ret', ret)
    #     return ret

    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's free on the target storage system and
        available for new content to be written to.
        """
        from django.core.exceptions import SuspiciousFileOperation
        from django.utils.crypto import get_random_string
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # If the filename already exists, add an underscore and a random 7
        # character alphanumeric string (before the file extension, if one
        # exists) to the filename until the generated filename doesn't exist.
        # Truncate original name if required, so the new filename does not
        # exceed the max_length.
        name = os.path.join(dir_name, "%s_%s%s" % (file_root, get_random_string(7), file_ext))
        while self.exists(name) or (max_length and len(name) > max_length):
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s_%s%s" % (file_root, get_random_string(7), file_ext))
            if max_length is None:
                continue
            # Truncate file_root if max_length exceeded.
            truncation = len(name) - max_length
            if truncation > 0:
                file_root = file_root[:-truncation]
                # Entire file_root was truncated in attempt to find an available filename.
                if not file_root:
                    raise SuspiciousFileOperation(
                        'Storage can not find an available filename for "%s". '
                        'Please make sure that the corresponding file field '
                        'allows sufficient "max_length".' % name
                    )
                name = os.path.join(dir_name, "%s_%s%s" % (file_root, get_random_string(7), file_ext))
        return name


fs = FileStorage()


# settings.DEFAULT_FILE_STORAGE = FileStorage


# Create your models here.


class Record(models.Model):
    FORMATE_CHOICES = (
        (1, 'CD'),
        (2, 'LP'),
        (3, 'MC'),
        (4, 'DATA')
    )

    title = models.CharField(max_length=128, verbose_name='标题')
    number = models.CharField(max_length=128, blank=True, null=True, verbose_name='编号')

    format = models.IntegerField(choices=FORMATE_CHOICES, blank=True, null=True, verbose_name='介质')
    release = models.CharField(max_length=8, blank=True, null=True, verbose_name='发布时间', help_text='yyyy')

    producer = models.CharField(max_length=128, blank=True, null=True, verbose_name='监制')
    release_order = models.CharField(max_length=8, blank=True, null=True, verbose_name='发布时间排序', help_text='yyyy0000')
    recorder = models.CharField(max_length=128, blank=True, null=True, verbose_name='录音')
    mixer = models.CharField(max_length=128, blank=True, null=True, verbose_name='混音')
    bandsman = models.TextField(blank=True, null=True, verbose_name='乐手')
    description = models.TextField(blank=True, null=True, verbose_name='说明')

    artists = models.ManyToManyField('Artist', blank=True, verbose_name='歌手')
    company = models.ForeignKey('Company', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='唱片公司')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def format_value(self):
        for choice in Record.FORMATE_CHOICES:
            if self.format == choice[0]:
                return choice[1]
        return None

    @classmethod
    def format_value_to_key(cls, value):
        for choice in Record.FORMATE_CHOICES:
            if value == choice[1]:
                return choice[0]
        return None

    def dirname(self):
        from .util import lx_quote
        dirname = '[{title}][{number}]'.format(title=lx_quote(self.title), number=lx_quote(self.number))
        return dirname

    def __unicode__(self):
        return self.title
        # return unicode(self.name, 'utf-8')

    def __str__(self):
        return 'Record({}, {})'.format(self.title, self.number)

    def delete(self, using=None, keep_parents=False):
        print('Record', 'delete')
        super(Record, self).delete(using, keep_parents)

    class Meta:
        ordering = ['release', 'release_order', 'title']


# class PersonTable(tables.Table):
#     selection = tables.CheckBoxColumn(accessor='pk', orderable=False)
#
#     class Meta:
#         model = Person
#         sequence = ('selection', 'first_name', 'last_name')


class Song(models.Model):
    track = models.CharField(max_length=128, verbose_name='序号')
    title = models.CharField(max_length=128, verbose_name='标题')
    lyricist = models.CharField(max_length=128, blank=True, null=True, verbose_name='作词')
    composer = models.CharField(max_length=128, blank=True, null=True, verbose_name='作曲')
    arranger = models.CharField(max_length=128, blank=True, null=True, verbose_name='编曲')
    vocalist = models.CharField(max_length=128, blank=True, null=True, verbose_name='和音')
    producer = models.CharField(max_length=128, blank=True, null=True, verbose_name='监制')
    bandsman = models.TextField(blank=True, null=True, verbose_name='乐手')
    description = models.TextField(blank=True, null=True, verbose_name='说明')

    artists = models.ManyToManyField('Artist', blank=True, verbose_name='歌手')
    record = models.ForeignKey('Record', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#{track} - {title}'.format(track=self.track, title=self.title)

    class Meta:
        order_with_respect_to = 'record'
        # ordering = ['title']


class Artist(models.Model):
    TYPE_CHOICES = (
        (1, '男歌手'),
        (0, '女歌手'),
        (2, '组合')
    )

    name = models.CharField(max_length=128, verbose_name='名称')
    type = models.IntegerField(choices=TYPE_CHOICES, blank=True, null=True, verbose_name='类型')

    # records = models.ManyToManyField('Record', blank=True, verbose_name='专辑')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def type_value(self):
        for choice in Artist.TYPE_CHOICES:
            if self.type == choice[0]:
                return choice[1]
        return self.type

    @classmethod
    def type_value_to_key(cls, value):
        for choice in Artist.TYPE_CHOICES:
            if value == choice[1]:
                return choice[0]
        return None

    def dirname(self):
        from .util import lx_quote
        dirname = '[{name}]'.format(name=lx_quote(self.name))
        return dirname

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{name}'.format(name=self.name)

    def delete(self, using=None, keep_parents=False):
        print('Artist', 'delete')
        super(Artist, self).delete(using, keep_parents)

    class Meta:
        ordering = ['name']


class Company(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{name}'.format(name=self.name)

    class Meta:
        ordering = ['name']


def record_cover_upload_to(instance, filename):
    record = instance.record

    record_dirname = record.dirname()
    import portal.util as util
    extension = util.get_extension(filename)

    format = 'record/{record_dirname}/{record_dirname}{extension}'

    upload_to = format.format(record_dirname=record_dirname,
                              extension=extension)

    print('record_cover_upload_to', 'upload_to', upload_to)

    return upload_to


class RecordCover(models.Model):
    record = models.OneToOneField('Record', on_delete=models.CASCADE)

    image = models.ImageField(upload_to=record_cover_upload_to, height_field='height', width_field='width',
                              null=True, verbose_name='图片', storage=fs)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_exists(self):
        return fs.exists(self.image.name)

    def delete(self, using=None, keep_parents=False):
        print('RecordCover', 'delete')
        print('RecordCover', 'self.image', self.image)
        try:
            self.image.delete()
        except:
            pass
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print('RecordCover', 'save')
        try:
            this = RecordCover.objects.get(pk=self.id)
            this.image.delete()
        except:
            pass
        super().save(force_insert, force_update, using,
                     update_fields)


def record_images_upload_to(instance, filename):
    record = instance.record

    record_dirname = record.dirname()
    import portal.util as util
    extension = util.get_extension(filename)

    format = 'record/{record_dirname}/{record_dirname}{extension}'
    upload_to = format.format(record_dirname=record_dirname,
                              extension=extension)

    return upload_to


class RecordImages(models.Model):
    record = models.ForeignKey('Record', on_delete=models.CASCADE)

    image = models.ImageField(upload_to=record_images_upload_to, height_field='height', width_field='width',
                              null=True, verbose_name='图片', storage=fs)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_exists(self):
        return fs.exists(self.image.name)

    def delete(self, using=None, keep_parents=False):
        print('RecordImages', 'delete')
        print('RecordImages', 'self.image', self.image)
        try:
            self.image.delete()
        except:
            pass
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print('RecordImages', 'save')
        try:
            this = RecordImages.objects.get(pk=self.id)
            this.image.delete()
        except:
            pass
        super().save(force_insert, force_update, using,
                     update_fields)


def artist_avatar_upload_to(instance, filename):
    artist = instance.artist

    artist_dirname = artist.dirname()
    import portal.util as util
    extension = util.get_extension(filename)

    format = 'artist/{artist_dirname}/{artist_dirname}(0){extension}'

    upload_to = format.format(artist_dirname=artist_dirname,
                              extension=extension)

    return upload_to


class ArtistAvatar(models.Model):
    artist = models.OneToOneField('Artist', on_delete=models.CASCADE)

    image = models.ImageField(upload_to=artist_avatar_upload_to, height_field='height', width_field='width',
                              null=True, verbose_name='图片', storage=fs)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_exists(self):
        return fs.exists(self.image.name)

    def delete(self, using=None, keep_parents=False):
        print('ArtistAvatar', 'delete')
        print('ArtistAvatar', 'self.image', self.image)
        try:
            self.image.delete()
        except:
            pass
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print('ArtistAvatar', 'save')
        try:
            this = ArtistAvatar.objects.get(pk=self.id)
            this.image.delete()
        except:
            pass
        super().save(force_insert, force_update, using,
                     update_fields)


def artist_images_upload_to(instance, filename):
    artist = instance.artist

    print('instance.artist', instance.artist)

    artist_dirname = artist.dirname()
    import portal.util as util
    extension = util.get_extension(filename)

    format = 'artist/{artist_dirname}/{artist_dirname}{extension}'
    upload_to = format.format(artist_dirname=artist_dirname,
                              extension=extension)

    return upload_to


class ArtistImages(models.Model):
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)

    image = models.ImageField(upload_to=artist_images_upload_to, height_field='height', width_field='width',
                              null=True, verbose_name='图片', storage=fs)

    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_exists(self):
        return fs.exists(self.image.name)

    def delete(self, using=None, keep_parents=False):
        print('ArtistImages', 'delete')
        print('ArtistImages', 'self.image', self.image)
        try:
            self.image.delete()
        except:
            pass
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print('ArtistImages', 'save')
        try:
            this = ArtistImages.objects.get(pk=self.id)
            this.image.delete()
        except:
            pass
        super().save(force_insert, force_update, using,
                     update_fields)


class ExcelLog(models.Model):
    STATUS_START = 0
    STATUS_SUCCESS = 1
    STATUS_ERROR = -1

    STATUS_CHOICES = (
        (0, '开始'),
        (1, '成功'),
        (-1, '失败')
    )

    datetime_start = models.DateTimeField(null=True)
    datetime_end = models.DateTimeField(null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, blank=True, null=True)

    file_excel = models.FileField(null=True)
    file_log = models.FileField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-datetime_start']
