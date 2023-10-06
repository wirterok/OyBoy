from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"history", views.ViewHistoryViewSet)
router.register(r"channel", views.ProfileViewSet)
