from rest_framework.routers import DefaultRouter

from .views import HearingViewSet

router = DefaultRouter()
router.register("hearings", HearingViewSet, basename="hearing")

urlpatterns = router.urls
