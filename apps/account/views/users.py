from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.account.models import CustomUser
from apps.account.serializers.users import UserSerializers
from apps.account.permission import IsProfileOwner


class UserApiView(ModelViewSet):
    serializer_class = UserSerializers
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]
