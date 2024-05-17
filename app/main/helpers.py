import logging
import traceback
from datetime import date, timedelta, datetime
from typing import Tuple

from django.contrib.admin import DateFieldListFilter
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.paginator import Paginator, Page
from django.core.signing import Signer
from django.db.models import QuerySet, Q
from django.utils import timezone

logger = logging.getLogger(__name__)


def try_exc(name):
    """
    Декоратор для логгирования исключений через logging
    """
    logger_instance = logging.getLogger(name)

    def decorator(func):
        def _wrapper(request=None, *args, **kwargs):
            try:
                response = (
                    func(request, *args, **kwargs)
                    if request is not None
                    else func(*args, **kwargs)
                )
            except:
                if hasattr(request, "build_absolute_uri"):
                    path = request.build_absolute_uri()
                else:
                    path = ""
                logger_instance.error(
                    msg=f"{name} - {path}", exc_info=traceback.format_exc()
                )
            else:
                return response

        return _wrapper

    return decorator


class MyDateTimeFilter(DateFieldListFilter):
    '''
    Расширяет фильтр даты админки, добавляет: вчера, прошлый месяц
    '''
    def __init__(self, *args, **kwargs):
        super(MyDateTimeFilter, self).__init__(*args, **kwargs)

        now = timezone.now()

        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()

        date_end = today.replace(day=1)

        last_day_of_prev_month = date_end - timedelta(days=1)

        start_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        self.links += (
            (
                ("Прошлый месяц"),
                {
                    self.lookup_kwarg_since: str(start_day_of_prev_month),
                    self.lookup_kwarg_until: str(date_end),
                },
            ),
        )

        today = now.date()
        self.links += (
            (
                ("Вчера"),
                {
                    self.lookup_kwarg_since: str(today - timedelta(days=1)),
                    self.lookup_kwarg_until: str(today),
                },
            ),
        )
