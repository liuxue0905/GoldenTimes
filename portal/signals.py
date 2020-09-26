from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import RecordCover, RecordImages, ArtistAvatar, ArtistImages


@receiver(pre_save, sender=RecordCover)
def receiver_pre_save_record_cover(sender, **kwargs):
    print("receiver_pre_save_record_cover")
    print("receiver_pre_save_record_cover", "kwargs", kwargs)

    signal = kwargs['signal']
    instance: RecordCover = kwargs['instance']
    using = kwargs['using']

    try:
        # instance.image.delete()
        instance.image.file.delete()
    except:
        pass
    finally:
        pass


@receiver(post_delete, sender=RecordCover)
def receiver_post_delete_record_cover(sender, **kwargs):
    print("receiver_post_delete_record_cover")
    print("receiver_post_delete_record_cover", 'kwargs', kwargs)

    signal = kwargs['signal']
    instance = kwargs['instance']
    using = kwargs['using']

    try:
        instance.image.file.delete()
    except:
        pass
    finally:
        pass


@receiver(post_delete, sender=RecordImages)
def receiver_post_delete_record_images(sender, **kwargs):
    print("receiver_post_delete_record_images")


@receiver(pre_save, sender=ArtistAvatar)
def receiver_pre_save_artist_avatar(sender, **kwargs):
    print("receiver_pre_save_artist_avatar")
    print("receiver_pre_save_artist_avatar", 'kwargs', kwargs)


@receiver(post_delete, sender=ArtistAvatar)
def receiver_post_delete_artist_avatar(sender, **kwargs):
    print("receiver_post_delete_artist_avatar")


@receiver(post_delete, sender=ArtistImages)
def receiver_post_delete_artist_images(sender, **kwargs):
    print("receiver_post_delete_artist_images")
