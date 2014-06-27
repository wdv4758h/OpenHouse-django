# -*- coding: utf-8 -*-

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailforms.models import AbstractFormField, AbstractForm
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet

from datetime import date

# Index Page

class YearIndex(Page):
    body = RichTextField('內文', blank=True)

    search_name = '首頁'

    subpage_types = ('RdssIndex', 'RecruitIndex', 'HrdbIndex', 'NewsIndex')

    def __init__(self, *args, **kwargs):
        year = str(date.today().year + 1)
        self._meta.get_field('title').default           = year
        self._meta.get_field('slug').default            = year
        self._meta.get_field('show_in_menus').default   = False
        super(YearIndex, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '每年首頁'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

# Rdss Pages

class RdssIndex(Page):
    sub_title = models.CharField('副標', max_length=255, blank=True, help_text='副標')
    body = RichTextField('內文', blank=True)

    search_name = '研發替代役'

    subpage_types = ('TeachIndex', )

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = '研發替代役'
        self._meta.get_field('slug').default            = 'rdss'
        self._meta.get_field('show_in_menus').default   = True
        super(RdssIndex, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '研發替代役 - 首頁'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

# Recruit Pages

class RecruitIndex(Page):
    sub_title = models.CharField('副標', max_length=255, blank=True, help_text='副標')
    body = RichTextField('內文')

    search_name = '校園徵才'

    subpage_types = ('TeachIndex', )

    def __init__(self, *args, **kwargs):
        self._meta.get_field('slug').default            = 'recruit'
        self._meta.get_field('title').default           = '校園徵才'
        self._meta.get_field('show_in_menus').default   = True
        super(RecruitIndex, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '校園徵才 - 首頁'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

# News Pages

class NewsIndex(Page):
    sub_title = models.CharField('副標', max_length=255, blank=True)
    body = RichTextField('內文', blank=True)

    search_name = '公告'

    subpage_types = ('News', )

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    def __init__(self, *args, **kwargs):
        self._meta.get_field('slug').default            = 'news'
        self._meta.get_field('title').default           = '最新公告'
        self._meta.get_field('show_in_menus').default   = True
        super(NewsIndex, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '公告 - 首頁'

    def news(self):
        # Get list of live News that are descendants of this page
        news = News.objects.live().descendant_of(self)

        # Order by create time
        news = news.order_by('-create_time')

        return news

class News(Page):
    body = RichTextField('內文')
    create_time = models.DateTimeField('發佈時間', auto_now_add=True)
    update_time = models.DateTimeField('更新時間', auto_now=True)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('slug').default            = ''
        self._meta.get_field('title').default           = ''
        self._meta.get_field('show_in_menus').default   = False
        super(News, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '公告'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

# Hrdb Pages

class HrdbIndex(Page):
    body = RichTextField('內文', blank=True)
    pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='條款檔案 (PDF)'
    )

    search_name = '人才庫'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('slug').default            = 'hrdb'
        self._meta.get_field('title').default           = '交大人才庫'
        self._meta.get_field('show_in_menus').default   = True
        super(HrdbIndex, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '人才庫 - 首頁'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname='full'),
        DocumentChooserPanel('pdf'),
    ]

class HrdbFormField(AbstractFormField):
    page = ParentalKey('HrdbForm', related_name='form_fields')

class HrdbForm(AbstractForm):
    explain = RichTextField('說明', blank=True)

    class Meta:
        verbose_name = '人才庫 - 表單'

HrdbForm.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('explain', classname='full'),
    InlinePanel(HrdbForm, 'form_fields', label="Form fields"),
]
