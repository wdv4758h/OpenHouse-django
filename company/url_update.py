#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Q
from company.models import Company

for i in Company.objects.filter(~Q(website__startswith='http')):
    i.website = 'http://' + i.website.strip()
    i.save()
