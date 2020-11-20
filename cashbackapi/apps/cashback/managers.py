from django.db import models
from django.db.models.functions import Trunc
from django.db.models import Sum


class CashbackManager(models.Manager):

    def get_queryset(self):
        qs = super(CashbackManager, self).get_queryset().annotate(
            value_month=Trunc('date', 'month')
        ).values('value_month').annotate(total=Sum('amount'))
        return qs
