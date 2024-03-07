from django.urls import path


from .views import PublicPostViewSet, PostViewSet, CommentApiView


urlpatterns = [
    path("public-posts/", PublicPostViewSet.as_view({"get": "list"})),
    path("public-posts/<int:pk>/", PublicPostViewSet.as_view({"get": "retrieve"})),
    path("posts/", PostViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "posts/<int:pk>/",
        PostViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
    ),
    path("comments/", CommentApiView.as_view()),
]
