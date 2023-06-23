from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False, blank=False)
    label = models.TextField(max_length=100, blank=True, default='')
    text = RichTextUploadingField()
    post_image = models.ImageField(upload_to='blog_posts', default='')
    date = models.DateField(blank=False, default=timezone.now)

    def __str__(self):
        return self.title

class CommentModel(models.Model):
    comment = models.TextField(max_length=500, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogPost = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment

class CommentOfComment(models.Model):
    text = models.TextField(max_length=500, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentModel, related_name='comment2', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    blogPost = models.ForeignKey(BlogPost, related_name='comments2', on_delete=models.CASCADE)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text