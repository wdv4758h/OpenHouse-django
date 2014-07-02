# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.core import urlresolvers

from wagtail.wagtailadmin import hooks
from wagtail.wagtailadmin.menu import MenuItem

from hrdb import urls


def register_admin_urls():
    return [
        url(r'^hrdb/', include(urls)),
    ]
hooks.register('register_admin_urls', register_admin_urls)


def construct_main_menu(request, menu_items):
    #if request.user.has_module_perms('auth'):
    if True:
        menu_items.append(
            MenuItem(u'人才庫', urlresolvers.reverse('hrdb_index'), classnames='icon icon-user', order=600)
        )
hooks.register('construct_main_menu', construct_main_menu)
