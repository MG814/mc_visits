import factory

from .models import DoctorAvailability


class DoctorAvailabilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DoctorAvailability

    doctor_id = factory.Faker('random_int', min=1, max=10)
    date = factory.Faker('date')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    available_hours = factory.Dict({
        "8": True,
        "9": False,
        "10": True
    })
