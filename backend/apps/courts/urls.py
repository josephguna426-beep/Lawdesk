from rest_framework.routers import DefaultRouter

from .views import AdvocateViewSet, CourtViewSet

router = DefaultRouter()
router.register("courts", CourtViewSet, basename="court")
router.register("advocates", AdvocateViewSet, basename="advocate")

urlpatterns = router.urls
