import io
import imghdr

from PIL import Image

from mitmproxy.types import multidict
from . import image_parser

from mitmproxy.contentviews import base


class ViewImage(base.View):
    name = "Image"
    prompt = ("image", "i")
    content_types = [
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/vnd.microsoft.icon",
        "image/x-icon",
    ]

    def __call__(self, data, **metadata):
        image_type = imghdr.what('', h=data)
        if image_type == 'png':
            f = "PNG"
            parts = image_parser.parse_png(data)
            fmt = base.format_dict(multidict.MultiDict(parts))
            return "%s image" % f, fmt
        elif image_type == 'gif':
            f = "GIF"
            parts = image_parser.parse_gif(data)
            fmt = base.format_dict(multidict.MultiDict(parts))
            return "%s image" % f, fmt
        elif image_type == 'jpeg':
            f = "JPEG"
            parts = image_parser.parse_jpeg(data)
            fmt = base.format_dict(multidict.MultiDict(parts))
            return "%s image" % f, fmt
        try:
            img = Image.open(io.BytesIO(data))
        except IOError:
            return None
        parts = [
            ("Format", str(img.format_description)),
            ("Size", "%s x %s px" % img.size),
            ("Mode", str(img.mode)),
        ]
        for i in sorted(img.info.keys()):
            if i != "exif":
                parts.append(
                    (str(i), str(img.info[i]))
                )
        fmt = base.format_dict(multidict.MultiDict(parts))
        return "%s image" % img.format, fmt
