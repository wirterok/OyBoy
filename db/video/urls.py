from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r"comment", views.CommentViewSet)
router.register(r"video", views.VideoViewSet)
router.register(r"favourite", views.FavouriteViewSet)
router.register(r"like", views.LikeViewSet)
router.register(r"dislike", views.DislikeViewSet)
router.register(r"view", views.ViewViewSet)
router.register(r"tag", views.TagViewSet)
router.register(r"suggestion", views.SearchHistoryViewSet)
