# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin import hooks
from wagtail.wagtailadmin.menu import MenuItem

from staff import urls


def register_admin_urls():
    return [
        url(r'^staffs/', include(urls)),
    ]
hooks.register('register_admin_urls', register_admin_urls)


def construct_main_menu(request, menu_items):
    #if request.user.has_module_perms('auth'):
    if True:
        menu_items.append(
            MenuItem(_(u'工作人員'), urlresolvers.reverse('staff_index'), classnames='icon icon-user', order=600)
        )
hooks.register('construct_main_menu', construct_main_menu)
