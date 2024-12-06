import factory

from .models import Visit


class VisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Visit

    patient_id = factory.Faker('random_int', min=1, max=10)
    doctor_id = factory.Faker('random_int', min=1, max=10)
    date = factory.Faker('date_time')
    title = factory.Faker('text', max_nb_chars=50)
