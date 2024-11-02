from rest_framework import routers

from .views import DoctorAvailabilityView

router = routers.SimpleRouter()
router.register('doctor-availabilities', DoctorAvailabilityView, basename='availability')


urlpatterns = [
]
urlpatterns += router.urls
