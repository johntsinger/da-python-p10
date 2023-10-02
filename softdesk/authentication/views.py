from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from authentication.permissions import (
    IsAdmin,
    IsOwner
)
from authentication.serializers import (
    UserDetailSerializer,
)


User = get_user_model()


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdmin]
        elif self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsOwner | IsAdmin]
        return super().get_permissions()
