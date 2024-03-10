from django.utils import timezone
from apps.account.serializers.follow import UserSerializers
from apps.post.serializers.post_category import PostCategorySerializer
from ..models import Post

from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    minutes_to_read = serializers.SerializerMethodField()
    time_since_created = serializers.SerializerMethodField()

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
            "minutes_to_read",
            "time_since_created",
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

    def get_minutes_to_read(self, obj):
        words_per_minute = 200
        total_words = len(obj.content.split())
        minutes_to_read = max(1, total_words / words_per_minute)
        return round(minutes_to_read)

    def get_time_since_created(self, obj):
        created_at = obj.created_at
        now = timezone.now()
        time_difference = now - created_at

        if time_difference.days == 0:
            # If created today, show hours and minutes ago
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            if hours > 0:
                return f"{hours} hrs ago"
            elif minutes > 0:
                return f"{minutes} mins ago"
            else:
                return "Just now"
        elif 0 < time_difference.days < 7:
            # If created within the past week, show days ago
            return f"{time_difference.days} days ago"
        else:
            # If created more than a week ago, show the date
            return created_at.strftime("%b %d, %Y")

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
