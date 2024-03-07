from ..models import Comment, Post
from ..serializers import CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class CommentApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            post_id = request.GET.get("post_id", None)
            if post_id:
                post = Post.objects.get(id=post_id)
                queryset = Comment.objects.filter(post=post, parent_comment=None)
                serializer = CommentSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response(
                    "Post id is required", status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
