from imagekit.specs import ImageSpec
from imagekit.processors import TrimBorderColor, Adjust
from portal.imagekit.watermark import ImageWatermark

# watermark = Image.open("200-star.png")
# if you use a file-like object
# remember to close your file when done
watermark = open("200-star.png")

watermark = ImageWatermark(watermark,
                           position=('center', 'center'),
                           scale=True,
                           repeat=False,
                           opacity=0.2),


class MySpec(ImageSpec):
    processors = [
        TrimBorderColor(),
        Adjust(contrast=1.2, sharpness=1.1),
        watermark
    ]
    format = 'JPEG'
    options = {'quality': 60}
