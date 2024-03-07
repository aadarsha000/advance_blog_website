from ..models import CustomUser, UserFollowing
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "full_name",
            "avatar",
        ]


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["following_user_id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.method == "GET":
            user_data = UserSerializers(instance.following_user_id).data

            data["following_user_id"] = user_data
        return data


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["user_id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.method == "GET":
            user_data = UserSerializers(instance.user_id).data

            data["user_id"] = user_data
        return data
