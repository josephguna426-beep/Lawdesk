from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, PartyViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet, basename="client")
router.register("parties", PartyViewSet, basename="party")

urlpatterns = router.urls
