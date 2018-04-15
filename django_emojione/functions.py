__author__ = "phuong"
__date__ = "03 31 2016, 3:05 PM"

import re

from django.conf import settings
from emojipy import Emoji
from emojipy.ruleset import shortcode_replace, ascii_replace, category_replace
from .ruleset import unicode_replace

from html import escape


class CustomEmoji(Emoji):
    ignored_regexp = '<object[^>]*>.*?<\/object>|<span[^>]*>.*?<\/span>|<(?:object|embed|svg|img|div|span|p|a)[^>]*>'
    unicode_regexp = "(" + '|'.join(
        [re.escape(x.decode("utf-8")) for x in sorted(unicode_replace.keys(), key=len, reverse=True)]) + ")"
    unicode_compiled = re.compile(ignored_regexp + "|(" + unicode_regexp + ")", re.UNICODE)

    @classmethod
    def unicode_to_image(cls, text, **kwargs):
        css_class = kwargs.pop('css', '')
        style = kwargs.pop('style', '')

        def replace_unicode(match):
            unicode_char = text[match.start():match.end()]
            unicode_encoded = unicode_char.encode('utf-8')
            if not unicode_encoded or unicode_encoded not in unicode_replace:
                return unicode_char  # unsupported unicode char
            shortcode = unicode_replace[unicode_encoded]
            if cls.unicode_alt:
                alt = unicode_char
            else:
                alt = shortcode
            filename = shortcode_replace[shortcode]
            category = category_replace[shortcode]

            if cls.sprites:
                return '<span class="emojione emojione-32-%s _%s" title="%s">%s</span>' \
                       % (category, filename, escape(shortcode), alt)
            else:
                return '<img class="emojione %s" style="%s" alt="%s" src="%s"/>' % (
                    css_class, style, alt,
                    cls.image_png_path + filename + '.png'
                )

        text = re.sub(cls.unicode_compiled, replace_unicode, text)
        return text


image_type = 'png'
if hasattr(settings, 'EMOJIPY_IMAGE_TYPE'):
    image_type = settings.EMOJIPY_IMAGE_TYPE

if hasattr(settings, 'EMOJIPY_SPRITES'):
    Emoji.sprites = settings.EMOJIPY_SPRITES

if hasattr(settings, 'EMOJIPY_SPRITES_PATH'):
    Emoji.image_path_svg_sprites = settings.EMOJIPY_SPRITES_PATH

Emoji.image_type = image_type
if hasattr(settings, 'EMOJIPY_IMAGE_PATH'):
    if image_type is 'png':
        Emoji.image_png_path = settings.EMOJIPY_IMAGE_PATH
    elif image_type is 'svg':
        Emoji.image_svg_path = settings.EMOJIPY_IMAGE_PATH


def to_image(text, **kwargs):
    """
    Parse short code and unicode code to emotion
    :param text:
    :param kwargs[css]: css class
    :param kwargs[style]: icon stylesheet
    :return: string
    """
    return CustomEmoji.to_image(text, **kwargs)


def unicode_to_image(text, **kwargs):
    return CustomEmoji.unicode_to_image(text, **kwargs)


def ascii_to_unicode(text, **kwargs):
    return Emoji.ascii_to_unicode(text, **kwargs)


def ascii_to_image(text, **kwargs):
    return Emoji.ascii_to_image(text, **kwargs)


def shortcode_to_image(text, **kwargs):
    return Emoji.shortcode_to_image(text, **kwargs)
