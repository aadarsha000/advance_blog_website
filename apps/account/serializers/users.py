from ..models import CustomUser, UserFollowing

from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    total_following = serializers.SerializerMethodField()
    total_follower = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "full_name",
            "avatar",
            "dob",
            "address",
            "city",
            "state",
            "country",
            "phone_number",
            "total_following",
            "total_follower",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
        }

    def get_total_following(self, obj):
        return UserFollowing.objects.filter(user_id=obj).count()

    def get_total_follower(self, obj):
        return UserFollowing.objects.filter(following_user_id=obj).count()
