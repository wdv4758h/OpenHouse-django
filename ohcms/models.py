# -*- coding: utf-8 -*-

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

class YearIndex(Page):
    body = RichTextField()

    search_name = "首頁"

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname="full"),
    ]

class RdssIndex(Page):
    body = RichTextField()

    search_name = "研發替代役"

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname="full"),
    ]

class RecruitIndex(Page):
    sub_title = models.CharField(max_length=255, help_text='副標')
    body = RichTextField()

    search_name = "校園徵才"

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname="full"),
    ]

class NewsIndex(Page):
    sub_title = models.CharField(max_length=255, help_text='副標')
    body = RichTextField()

    search_name = "公告"

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname="full"),
    ]

    def news(self):
        # Get list of live News that are descendants of this page
        news = News.objects.live().descendant_of(self)

        # Order by create time
        news = news.order_by('-create_time')

        return news

class News(Page):
    body = RichTextField()
    create_time = models.DateTimeField('發佈時間', auto_now_add=True)
    update_time = models.DateTimeField('更新時間', auto_now=True)

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname="full"),
    ]

class HrdbIndex(Page):
    body = RichTextField()

    search_name = "人才庫"

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname="full"),
    ]
