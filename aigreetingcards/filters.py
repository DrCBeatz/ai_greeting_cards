# aigreetingcards/filters.py

import django_filters
from .models import Image
from django.utils.translation import gettext as _
from django.db.models import Q

class ImageFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='image_text_filter', label='Search')

    class Meta:
        model = Image
        fields = ['search']

        def image_text_filter(self, queryset, name, value):
            return Image.objects.filter(
                Q(title__icontains=value) | Q(user__username__icontains=value)
            )
