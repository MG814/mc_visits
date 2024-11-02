from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from core import settings
from visits.models import Visit
import logging
logger = logging.getLogger(__name__)


@shared_task
def send_visit_notification():
    logger.debug('rozpoczeto zadanie')
    tomorrow = timezone.now() + timedelta(days=1)
    visits = Visit.objects.filter(date__date=tomorrow.date())

    for visit in visits:
        user = visit.patient_id

        send_mail(
            'Przypomnienie o wizycie',
            f'Masz zaplanowaną wizytę na {visit.date.date()}, godzina {visit.date.time()}',
            settings.DEFAULT_EMAIL,
            ['sodemi9603@exweme.com'],
            fail_silently=False,
        )
