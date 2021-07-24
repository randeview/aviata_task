from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _  # noqa


class Cities(TextChoices):
    ALMATY = "Алматы", "Алматы"
    NUR_SULTAN = "Нур-Султан", "Нур-Султан"
