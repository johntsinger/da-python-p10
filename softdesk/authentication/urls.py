from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.urls import path, include
from authentication.views import AdminUserViewSet

router = routers.SimpleRouter()
router.register('user', AdminUserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token-refresh'),
    path('api/', include(router.urls))
]

"""
    path('api-auth/register/', RegisterView.as_view(),
         name='register'),
"""
