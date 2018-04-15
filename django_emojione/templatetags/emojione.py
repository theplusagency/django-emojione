__author__ = "phuong"
__date__ = "03 31 2016, 5:24 PM"

from django import template
from django.utils.safestring import mark_safe
from emojipy import Emoji
from django_emojione.functions import to_image as to_image_f, unicode_to_image as unicode_to_image_f

register = template.Library()


@register.simple_tag
def to_image(value, *args, **kwargs):
    return mark_safe(to_image_f(value, **kwargs))


@register.simple_tag
def unicode_to_image(value, *args, **kwargs):
    return mark_safe(unicode_to_image_f(value, **kwargs))


@register.simple_tag
def shortcode_to_image(value, *args, **kwargs):
    return mark_safe(Emoji.shortcode_to_image(value, **kwargs))


@register.simple_tag
def ascii_to_image(value, *args, **kwargs):
    return mark_safe(Emoji.ascii_to_image(value, **kwargs))


@register.simple_tag
def shortcode_to_unicode(value, *args, **kwargs):
    return mark_safe(Emoji.ascii_to_image(value, **kwargs))
