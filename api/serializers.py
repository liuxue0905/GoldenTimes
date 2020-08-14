from django.contrib.auth.models import User, Group
from rest_framework import serializers

from portal.models import Artist, Record, Song
from portal.models import Company

from django.db.models import Q


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ArtistListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    records_count = serializers.SerializerMethodField()
    songs_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        # fields = ['url', 'id', 'name', 'type', 'records_count', 'songs_count', 'comps_count', 'cover', 'image_list']
        fields = ['url', 'id', 'name', 'type', 'records_count', 'songs_count', 'cover']

    def get_records_count(self, obj):
        return obj.record_set.count()

    def get_songs_count(self, obj):
        return obj.song_set.count()

    def get_cover(self, obj):
        request = self.context.get('request')
        try:
            if obj.artistavatar and obj.artistavatar.image:
                return request.build_absolute_uri('/api/artists/{artist_id}/cover'.format(artist_id=obj.id))
        except:
            pass
        return None


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    records_count = serializers.SerializerMethodField()
    songs_count = serializers.SerializerMethodField()
    # comps_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        # fields = ['url', 'id', 'name', 'type', 'records_count', 'songs_count', 'comps_count', 'cover', 'image_list']
        fields = ['url', 'id', 'name', 'type', 'records_count', 'songs_count', 'cover', 'image_list']

    def get_records_count(self, obj):
        return obj.record_set.count()

    def get_songs_count(self, obj):
        return obj.song_set.count()

    def get_comps_count(self, obj):
        queryset = Record.objects.filter(~Q(artists__exact=obj), song__artists__exact=obj).distinct()
        return queryset.count()

    def get_cover(self, obj):
        request = self.context.get('request')
        try:
            if obj.artistavatar and obj.artistavatar.image:
                return request.build_absolute_uri('/api/artists/{artist_id}/cover'.format(artist_id=obj.id))
        except:
            pass
        return None

    def get_image_list(self, obj):
        from django.db.models.fields.files import ImageFieldFile
        request = self.context.get('request')
        try:
            queryset = obj.artistimages_set.all()

            results = []

            for image_model in queryset:
                try:
                    # print('image_model', image_model, image_model.id, image_model.image, image_model.width,
                    #       image_model.height)
                    image: ImageFieldFile = image_model.image

                    results.append(request.build_absolute_uri(
                        '/api/artists/{artist_id}/images/{image_id}'.format(artist_id=obj.id, image_id=image_model.id)))

                    # print('image', type(image), image, image.name, image.path)
                    # print('image', image.width, image.height)
                except:
                    pass

            return results
        except:
            return None


class ArtistFieldSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['url', 'id', 'name', 'cover']

    def get_cover(self, obj):
        request = self.context.get('request')
        try:
            if obj.artistavatar and obj.artistavatar.image:
                return request.build_absolute_uri('/api/artists/{artist_id}/cover'.format(artist_id=obj.id))
        except:
            pass
        return None


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class RecordSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField()
        cover = serializers.SerializerMethodField()

        class Meta:
            model = Record
            fields = ['url', 'id', 'title', 'cover']

        def get_cover(self, obj: Record):
            request = self.context.get('request')
            try:
                if obj.recordcover and obj.recordcover.image:
                    return request.build_absolute_uri('/api/records/{record_id}/cover'.format(record_id=obj.id))
            except:
                pass
            return None

    artists = ArtistFieldSerializer(many=True, read_only=True)
    record = RecordSerializer(read_only=True)

    class Meta:
        model = Song
        fields = ['url', 'id', 'track', 'title',
                  'lyricist', 'composer', 'arranger', 'vocalist', 'producer', 'bandsman', 'description',
                  'record', 'artists']


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class CompanySerializer(serializers.HyperlinkedModelSerializer):
        id = serializers.ReadOnlyField()

        class Meta:
            model = Company
            fields = ['url', 'id', 'name']

    class SongSerializer(serializers.HyperlinkedModelSerializer):
        artists = ArtistFieldSerializer(many=True, read_only=True)

        class Meta:
            model = Song
            fields = ['url', 'id', 'track', 'title',
                      'lyricist', 'composer', 'arranger', 'vocalist', 'producer', 'bandsman', 'description',
                      'artists']

    artists = ArtistFieldSerializer(many=True, read_only=True)
    company = CompanySerializer()
    songs = SongSerializer(source='song_set', many=True, read_only=True)
    songs_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ['url', 'id',
                  'title', 'number',
                  'format', 'year', 'release_detail', 'release_order', 'producer', 'recorder', 'mixer', 'bandsman',
                  'description',
                  'artists', 'company',
                  'songs', 'songs_count',
                  'cover', 'image_list']

    def get_songs_count(self, obj):
        return obj.song_set.count()

    def get_cover(self, obj: Record):
        request = self.context.get('request')
        try:
            if obj.recordcover and obj.recordcover.image:
                return request.build_absolute_uri('/api/records/{record_id}/cover'.format(record_id=obj.id))
        except:
            pass
        return None

    def get_image_list(self, obj):
        from django.db.models.fields.files import ImageFieldFile
        request = self.context.get('request')
        try:
            queryset = obj.recordimages_set.all()

            results = []

            for image_model in queryset:
                try:
                    # print('image_model', image_model, image_model.id, image_model.image, image_model.width,
                    #       image_model.height)
                    image: ImageFieldFile = image_model.image

                    results.append(request.build_absolute_uri(
                        '/api/records/{record_id}/images/{image_id}'.format(record_id=obj.id, image_id=image_model.id)))

                    # print('image', type(image), image, image.name, image.path)
                    # print('image', image.width, image.height)
                except:
                    pass

            return results
        except:
            return None


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    records_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['url', 'id', 'name', 'records_count']

    def get_records_count(self, obj):
        return obj.record_set.count()
