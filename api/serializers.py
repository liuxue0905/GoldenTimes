from django.contrib.auth.models import User, Group
from rest_framework import serializers

from portal.models import Artist, Record, Song
from portal.models import Company


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    records_count = serializers.SerializerMethodField()
    songs_count = serializers.SerializerMethodField()
    # comps_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['url', 'id', 'name', 'type', 'records_count', 'songs_count', 'cover',]

    def get_records_count(self, obj):
        return obj.record_set.count()

    def get_songs_count(self, obj):
        return obj.song_set.count()

    # def get_comps_count(self, obj):
    #     return obj.comp_set.count()

    def get_cover(self, obj):
        return None


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class ArtistSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField()

        class Meta:
            model = Artist
            fields = ['url', 'id', 'name']

    class RecordSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField()

        class Meta:
            model = Record
            fields = ['url', 'id', 'title']

    artists = ArtistSerializer(many=True, read_only=True)
    record = RecordSerializer(read_only=True)

    class Meta:
        model = Song
        fields = ['url', 'id', 'track', 'title',
                  'lyricist', 'composer', 'arranger', 'vocalist', 'producer', 'bandsman', 'description',
                  'record', 'artists']


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class ArtistSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField()

        class Meta:
            model = Artist
            fields = ['url', 'id', 'name']

    class CompanySerializer(serializers.HyperlinkedModelSerializer):
        id = serializers.ReadOnlyField()

        class Meta:
            model = Company
            fields = ['url', 'id', 'name']

    # class SongSerializer(serializers.HyperlinkedModelSerializer):
    #     class Meta:
    #         model = Song

    artists = ArtistSerializer(many=True, read_only=True)
    company = CompanySerializer()
    # song_set = SongSerializer(many=True, read_only=True)
    # songs = serializers.RelatedField(source='song_set', many=True, read_only=True)
    songs = SongSerializer(source='song_set', many=True, read_only=True)
    songs_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    # cover = serializers.Hyperlink()

    class Meta:
        model = Record
        fields = ['url', 'id',
                  'title', 'number',
                  'format', 'year', 'release_detail', 'release_order', 'producer', 'recorder', 'mixer', 'bandsman', 'description',
                  'artists', 'company',
                  'songs', 'songs_count',
                  'cover']

    def get_songs_count(self, obj):
        return obj.song_set.count()

    def get_cover(self, obj):
        # try:
        #     record: Record = obj
        #     cover = record.recordcover
        #     print('cover', cover)
        #     print('cover', cover.id, cover.image, cover.width, cover.height)
        # except Exception as e:
        #     print('except', e)
        #     pass
        return None


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    records_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['url', 'id', 'name', 'records_count']

    def get_records_count(self, obj):
        return obj.record_set.count()
