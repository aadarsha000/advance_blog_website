from rest_framework import serializers

from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "user",
            "text",
            "parent_comment",
            "created_at",
            "replies",
        )

    def get_replies(self, obj):
        replies_queryset = Comment.objects.filter(parent_comment=obj)
        replies_serializer = CommentSerializer(replies_queryset, many=True)
        return replies_serializer.data
