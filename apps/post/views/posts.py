from rest_framework import viewsets, permissions

from ..serializers import PostSerializer
from ..models import Post
from ..filters import PostFilter
from ..permission import IsPostOwnerOrReadOnly


class PublicPostViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = PostFilter
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    serializer_class = PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    filterset_class = PostFilter
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
