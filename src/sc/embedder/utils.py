# -*- coding: utf-8 -*-
from lxml import html
from sc.embedder.config import IFRAME_VALID_ATTRIBUTES


def sanitize_iframe_tag(code):
    """Remove invalid attributes from <iframe> tags.

    :param code: [required] HTML code to be sanitized.
    :type code: string
    :returns: valid HTML code.
    :rtype: string
    """
    sanitized_code = html.fromstring(code)
    for iframe in sanitized_code.xpath('//iframe'):
        for k, v in iframe.attrib.items():
            if k.lower() not in IFRAME_VALID_ATTRIBUTES:
                del(iframe.attrib[k])
            if not k.islower():
                iframe.attrib[k.lower()] = v
                del(iframe.attrib[k])

    return html.tostring(sanitized_code)


def validate_int_or_percentage(value):
    """Check if value is either a positive integer (less than 9999) or
    a percetage.

    :param value: number to be validated
    :type value: string
    :returns: True if value is valid
    :rtype: bool
    """
    try:
        return 0 < int(value) <= 9999
    except ValueError:
        if value.endswith('%'):
            try:
                return 0 < int(value[:-1]) <= 100
            except ValueError:
                return False
        return False
