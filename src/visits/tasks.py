from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from core import settings
from django.utils.timezone import localtime
from visits.models import Visit
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_visit_notification():
    logger.debug('rozpoczeto zadanie')
    tomorrow = timezone.now() + timedelta(days=1)
    visits = Visit.objects.filter(date__date=tomorrow.date())

    for visit in visits:
        patient_email = visit.patient_email
        local_dt = localtime(visit.date)

        send_mail(
            'Przypomnienie o wizycie',
            f'Masz zaplanowaną wizytę na {local_dt.date()}, godzina {local_dt.time().strftime("%H:%M")}',
            settings.DEFAULT_EMAIL,
            [patient_email],
            fail_silently=False,
        )
