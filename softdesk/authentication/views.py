from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from authentication.permissions import (
    IsAdminAuthenticated,
    IsThisMyData
)
from authentication.serializers import (
    UserSerializer,
)


User = get_user_model()


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [
                IsAdminAuthenticated
                | IsThisMyData
            ]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]
