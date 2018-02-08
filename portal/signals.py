from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import RecordCover, RecordImages, ArtistAvatar, ArtistImages


@receiver(post_delete, sender=RecordCover)
def receiver_post_delete_record_cover(sender, **kwargs):
    print("receiver_post_delete_record_cover")
    print("receiver_post_delete_record_cover", 'kwargs', kwargs)

    signal = kwargs['signal']
    instance = kwargs['instance']
    using = kwargs['using']

    # print("receiver_post_delete_record_cover", 'instance.image', type(instance.image), instance.image)

    # instance.image
    # < class 'django.db.models.fields.files.ImageFieldFile'>

    # if instance.image:
    #     instance.image.delete()


@receiver(post_delete, sender=RecordImages)
def receiver_post_delete_record_images(sender, **kwargs):
    print("receiver_post_delete_record_images")


@receiver(post_delete, sender=ArtistAvatar)
def receiver_post_delete_artist_avatar(sender, **kwargs):
    print("receiver_post_delete_artist_avatar")


@receiver(post_delete, sender=ArtistImages)
def receiver_post_delete_artist_images(sender, **kwargs):
    print("receiver_post_delete_artist_images")
