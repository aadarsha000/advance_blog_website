from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers import PostSerializer
from ..models import Post
from ..filters import PostFilter
from ..permission import IsPostOwnerOrReadOnly


class PublicPostViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = PostFilter
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    serializer_class = PostSerializer
    ordering = ["-created_at"]

    @action(detail=False, methods=["GET"])
    def order_by_likes(self, request):
        ordered_posts = self.get_queryset().order_by("-likes")
        page = self.paginate_queryset(ordered_posts)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(ordered_posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    filterset_class = PostFilter
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
