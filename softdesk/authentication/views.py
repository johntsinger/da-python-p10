from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from authentication.permissions import (
    IsAdminAuthenticated,
    IsStaffAuthenticated
)
from authentication.serializers import (
    UserSerializer,
)


User = get_user_model()


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]
