from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.account.models import UserFollowing
from apps.account.serializers import UserFollowingSerializer, UserFollowerSerializer


class UserFollowingViewSet(ModelViewSet):
    serializer_class = UserFollowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFollowing.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class UserFollowerViewSet(ModelViewSet):
    serializer_class = UserFollowerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFollowing.objects.filter(following_user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(following_user_id=self.request.user)
