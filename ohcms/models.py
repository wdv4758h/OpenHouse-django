# -*- coding: utf-8 -*-

from django.db import models
from django.template.response import TemplateResponse

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailforms.models import AbstractFormField, AbstractForm
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.utils import camelcase_to_underscore

from wagtail.wagtailsnippets.models import register_snippet

from hrdb.views import create as hrdb_create
from hrdb.forms import HrdbForm

from company.models import Company

from datetime import date, datetime

# Index Page

class YearIndex(Page):
    body = RichTextField('內文', blank=True)

    search_name = '首頁'

    subpage_types = ('RdssIndex', 'RecruitIndex', 'HrdbIndex', 'NewsIndex')

    def __init__(self, *args, **kwargs):
        year = str(date.today().year + 1)
        self._meta.get_field('title').default           = year
        self._meta.get_field('slug').default            = year
        self._meta.get_field('show_in_menus').default   = True
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

    subpage_types = ('TeachIndex', 'VisitIndex', 'JobFair', 'ForumIndex')

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

    subpage_types = ('TeachIndex', 'VisitIndex', 'JobFair', 'ForumIndex')

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

    subpage_types = tuple()

    class Meta:
        verbose_name = '公告'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

# Hrdb Pages

class HrdbIndex(Page):
    body = RichTextField('內文', blank=True)
    pdf  = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='條款檔案 (PDF)'
    )

    # Form
    form_title = models.CharField('表單標題', default='填寫資料',max_length=255)
    explain    = RichTextField('表單說明', blank=True)

    search_name = '人才庫'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('body', classname='full'),
        DocumentChooserPanel('pdf'),
        FieldPanel('form_title', classname='full'),
        FieldPanel('explain', classname='full'),
    ]

    class Meta:
        verbose_name = '人才庫 - 首頁 & 表單填寫'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('slug').default            = 'hrdb'
        self._meta.get_field('title').default           = '交大人才庫'
        self._meta.get_field('show_in_menus').default   = True
        super(HrdbIndex, self).__init__(*args, **kwargs)
        self.template_form = '{}/hrdb_form.html'.format(self._meta.app_label)
        self.template_form_fin = '{}/hrdb_form_landing.html'.format(self._meta.app_label)

    def serve(self, request, *args, **kwargs):
        try:
            if request.POST.getlist('agree'):
                if request.POST.getlist('agree')[0] == 'on':
                    context = self.get_context(request, *args, **kwargs)
                    context['form'] = HrdbForm
                    return TemplateResponse(request, self.template_form, context)
                else:
                    return super(HrdbIndex, self).serve(request)
            elif request.POST.getlist('name'):
                hrdb_create(request, create_only=True)
                return TemplateResponse(request, self.template_form_fin)
            else:
                return super(HrdbIndex, self).serve(request)
        except:
            return super(HrdbIndex, self).serve(request)

# Teach

class TeachIndex(Page):
    sub_title = models.CharField('副標', max_length=255, blank=True, default='企業職場導師講座報名')
    body = RichTextField('內文', blank=True)

    subpage_types = ('Teach', )

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = ''
        self._meta.get_field('slug').default            = 'teach'
        self._meta.get_field('show_in_menus').default   = True
        super(TeachIndex, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = '職場導師講座 - 首頁'

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    def teaches(self):
        teaches = Teach.objects.live().descendant_of(self).order_by('-start_time')
        return teaches

class Teach(Page):
    start_time  = models.DateTimeField('開始時間')
    end_time    = models.DateTimeField('結束時間')
    speaker     = models.CharField('主講人', max_length=20, blank=True)
    place       = models.CharField('地點', max_length=20, blank=True)
    mode        = models.CharField('進行方式', max_length=20, blank=True)
    body        = RichTextField('內文', blank=True)

    content_panels = [
        # company choose (WIP)
        FieldPanel('title', classname='full'),
        FieldPanel('start_time', classname='full'),
        FieldPanel('end_time', classname='full'),
        FieldPanel('speaker', classname='full'),
        FieldPanel('place', classname='full'),
        FieldPanel('mode', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    subpage_types = tuple()

    class Meta:
        verbose_name = '企業職場導師講座 - 報名'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = ''
        self._meta.get_field('slug').default            = ''
        self._meta.get_field('show_in_menus').default   = False
        super(Teach, self).__init__(*args, **kwargs)

    def in_time(self):
        end = '{}'.format(self.start_time)
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < end

class VisitIndex(Page):
    sub_title   = models.CharField('副標', max_length=255, blank=True, default='企業參訪報名')
    body        = RichTextField('內文', blank=True)

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    subpage_types = ('Visit', )

    class Meta:
        verbose_name = '企業參訪 - 首頁'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = ''
        self._meta.get_field('slug').default            = 'visit'
        self._meta.get_field('show_in_menus').default   = True
        super(VisitIndex, self).__init__(*args, **kwargs)

    def visits(self):
        visits = Visit.objects.live().descendant_of(self).order_by('-start_time')
        return visits

class Visit(Page):
    # need to change to choose company
    abbr        = models.CharField('公司簡稱', max_length=20, blank=True)
    limit       = models.CharField('限制科系', max_length=20, blank=True)
    body        = RichTextField('內文', blank=True)
    start_time  = models.DateTimeField('開始時間')
    end_time    = models.DateTimeField('結束時間')

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('abbr', classname='full'),
        FieldPanel('limit', classname='full'),
        FieldPanel('body', classname='full'),
        FieldPanel('start_time', classname='full'),
        FieldPanel('end_time', classname='full'),
    ]

    subpage_types = tuple()

    class Meta:
        verbose_name = '企業參訪 - 報名'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = ''
        self._meta.get_field('slug').default            = ''
        self._meta.get_field('show_in_menus').default   = False
        super(Visit, self).__init__(*args, **kwargs)

    def in_time(self):
        end = '{}'.format(self.start_time)
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < end

# Job Fair

class PositionCompany(models.Model):

    position = models.CharField('位置', max_length=5, blank=True)
    company  = models.ForeignKey(Company, related_name='+', verbose_name='廠商')

    panels = [
        FieldPanel('position', classname='full'),
        FieldPanel('company', classname='full'),
    ]

    class Meta:
        abstract = True

class PositionCompanyChoose(PositionCompany):
    page = ParentalKey('ohcms.JobFair', related_name='position_company')


class JobFair(Page):
    '''
    Model for Job Fair Company position choose
    '''
    sub_title   = models.CharField('副標', max_length=255, blank=True, default='就博會暨面談會')
    place       = models.CharField('地點', max_length=20, blank=True)
    image1      = models.ForeignKey(
                        'wagtailimages.Image',
                        null=True,
                        blank=True,
                        on_delete=models.SET_NULL,
                        related_name='+',
                        verbose_name='位置圖'
                    )

    image2      = models.ForeignKey(
                        'wagtailimages.Image',
                        null=True,
                        blank=True,
                        on_delete=models.SET_NULL,
                        related_name='+',
                        verbose_name='位置圖 2'
                    )
    body        = RichTextField('內文', blank=True)

    subpage_types = tuple()

    search_name = '位置圖'

    class Meta:
        verbose_name = '就博會'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = '就博會'
        self._meta.get_field('slug').default            = 'job'
        self._meta.get_field('show_in_menus').default   = True
        super(JobFair, self).__init__(*args, **kwargs)

JobFair.content_panels = [
    FieldPanel('title', classname='full'),
    FieldPanel('sub_title', classname='full'),
    FieldPanel('place', classname='full'),
    ImageChooserPanel('image1'),
    ImageChooserPanel('image2'),
    FieldPanel('body', classname='full'),
    InlinePanel(JobFair, 'position_company', label='位置'),
]

class ForumIndex(Page):
    sub_title   = models.CharField('副標', max_length=255, blank=True)
    body        = RichTextField('內文', blank=True)

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('sub_title', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    subpage_types = ('Forum', )

    class Meta:
        verbose_name = '加開講座 - 首頁'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = '加開講座報名'
        self._meta.get_field('slug').default            = 'forum'
        self._meta.get_field('show_in_menus').default   = True
        super(ForumIndex, self).__init__(*args, **kwargs)

    def forums(self):
        forums = Forum.objects.live().descendant_of(self).order_by('-start_time')
        return forums

class Forum(Page):
    # need to change to choose company
    abbr        = models.CharField('公司簡稱', max_length=20, blank=True)
    place       = models.CharField('地點', max_length=20, blank=True)
    start_time  = models.DateTimeField('開始時間')
    end_time    = models.DateTimeField('結束時間')
    body        = RichTextField('內文', blank=True)

    content_panels = [
        FieldPanel('title', classname='full'),
        FieldPanel('abbr', classname='full'),
        FieldPanel('place', classname='full'),
        FieldPanel('start_time', classname='full'),
        FieldPanel('end_time', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    subpage_types = tuple()

    class Meta:
        verbose_name = '企業職場導師講座 - 報名'

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default           = ''
        self._meta.get_field('slug').default            = ''
        self._meta.get_field('show_in_menus').default   = False
        super(Forum, self).__init__(*args, **kwargs)

    def in_time(self):
        end = '{}'.format(self.start_time)
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < end
