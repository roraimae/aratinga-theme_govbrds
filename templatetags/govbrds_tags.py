from math import floor
from urllib.parse import parse_qs, urlparse, urlunparse

from django import template
from django.contrib.messages import constants as message_constants
from django.template import Context
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from wagtail.models import Page
from ..core import get_govbrds_setting

MESSAGE_ALERT_TYPES = {
    message_constants.DEBUG: "warning",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "danger",
}

register = template.Library()

@register.simple_tag
def govbrds_setting(value):
    """
    Return django-govbrds setting for use in in a template.

    Please consider this tag private, do not use it in your own templates.
    """
    return get_govbrds_setting(value)

@register.simple_tag
def govbrds_server_side_validation_class(widget):
    """
    Return server side validation class from a widget.

    Please consider this tag private, do not use it in your own templates.
    """
    try:
        css_classes = _css_class_list([widget["attrs"]["class"]])
    except KeyError:
        return ""
    return " ".join([css_class for css_class in css_classes if css_class in ["is-valid", "is-invalid"]])


@register.simple_tag
def govbrds_classes(*args):
    """
    Return list of classes.

    Please consider this filter private, do not use it in your own templates.
    """
    return merge_css_classes(*args)


@register.filter
def govbrds_message_alert_type(message):
    """Return the alert type for a message, defaults to `info`."""
    try:
        level = message.level
    except AttributeError:
        pass
    else:
        try:
            return MESSAGE_ALERT_TYPES[level]
        except KeyError:
            pass
    return "info"


@register.simple_tag
def govbrds_javascript_url():
    """
    Return the full url to the govbrds JavaScript library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        govbrds_javascript_url

    **Usage**::

        {% govbrds_javascript_url %}

    **Example**::

        {% govbrds_javascript_url %}
    """
    return javascript_url()


@register.simple_tag
def govbrds_css_url():
    """
    Return the full url to the govbrds CSS library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        govbrds_css_url

    **Usage**::

        {% govbrds_css_url %}

    **Example**::

        {% govbrds_css_url %}
    """
    return css_url()


@register.simple_tag
def govbrds_theme_url():
    """
    Return the full url to a govbrds theme CSS library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        govbrds_theme_url

    **Usage**::

        {% govbrds_theme_url %}

    **Example**::

        {% govbrds_theme_url %}
    """
    return theme_url()


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the Foundation menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag("tags/top_menu.html", takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )
    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }

@register.inclusion_tag("tags/breadcrumb.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }