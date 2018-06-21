from imagekit.specs import ImageSpec, register
from imagekit.processors import TrimBorderColor, Adjust
from imagekit.processors import ResizeToCover, ResizeToFit
from portal.imagekit.watermark import ImageWatermark

from django.conf import settings
import os


# # any of these could be used
# watermark = "200-star.png"
# watermark = Image.open("200-star.png")
# watermark = open("200-star.png") # if you use a file-like object
#                                  # remember to close your file when done

# watermark = ImageWatermark(watermark,
#                            position=('center', 'center'),
#                            scale=True,
#                            repeat=False,
#                            opacity=0.2)

# class MySpec(ImageSpec):
#     processors = [
#         TrimBorderColor(),
#         Adjust(contrast=1.2, sharpness=1.1),
#         watermark
#     ]
#     format = 'JPEG'
#     options = {'quality': 60}


class ThumbnailDashboardSpec(ImageSpec):
    processors = [
        ResizeToCover(120, 120),
        ImageWatermark(os.path.join(settings.MEDIA_ROOT, 'watermarks/watermark.png'),
                       position=('bottom', 'right'),
                       scale=True,
                       repeat=False,
                       opacity=0.8)
    ]
    format = 'JPEG'
    options = {'quality': 60}


class ThumbnailSpec(ImageSpec):
    processors = [
        ResizeToCover(240, 240),
        ImageWatermark(os.path.join(settings.MEDIA_ROOT, 'watermarks/watermark.png'),
                       position=('bottom', 'right'),
                       scale=True,
                       repeat=False,
                       opacity=0.8)
    ]
    format = 'JPEG'
    options = {'quality': 60}


register.generator('myapp:thumbnail-dashboard', ThumbnailDashboardSpec)
register.generator('myapp:thumbnail', ThumbnailSpec)
