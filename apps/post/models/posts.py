from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    thumbnail = models.ImageField(upload_to="post/thumbnail")
    content = RichTextUploadingField()
    author = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    category = models.ManyToManyField("post.PostCategory")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
