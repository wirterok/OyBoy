from django.urls import path, include
from .video.urls import router as video_router
from .account.urls import router as account_router, views as account_views
from db import account

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("account/", include(account_router.urls)),
    path("video/", include(video_router.urls)),
    path("initial/", account_views.InitialView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]