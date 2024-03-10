from apps.account.serializers.follow import UserSerializers
from apps.post.serializers.post_category import PostCategorySerializer
from ..models import Post

from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "title",
            "thumbnail",
            "content",
            "category",
            "status",
            "author",
            "created_at",
            "updated_at",
            "number_of_likes",
            "is_liked",
        ]
        extra_kwargs = {
            "author": {"required": False},
        }

    def get_number_of_likes(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user
        return obj.likes.filter(id=user.id).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.method == "GET":
            user_data = UserSerializers(instance.author).data
            category_data = PostCategorySerializer(instance.category, many=True).data
            content_data = instance.content.replace("\r", "").replace("\n", "")
            data["author"] = user_data
            data["category"] = category_data
            data["content"] = content_data
        return data
