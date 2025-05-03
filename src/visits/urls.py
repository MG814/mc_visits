from rest_framework import routers

from .views import VisitView

router = routers.SimpleRouter()
router.register('visits', VisitView, basename='visit')

urlpatterns = router.urls
