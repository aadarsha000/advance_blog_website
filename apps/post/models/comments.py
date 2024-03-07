from django.db import models
from ckeditor.fields import RichTextField


class Comment(models.Model):
    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    text = RichTextField()
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text = f"Comment by {self.user.full_name} on {self.post.title}"
        if self.parent_comment:
            text = f"Reply by {self.user.full_name} on {self.parent_comment.user.full_name} to {self.post.title}"
        return text
