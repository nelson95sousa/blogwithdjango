from django.contrib import admin
from blog.models import BlogPost, CommentModel,CommentOfComment


# Register your models here.

admin.site.register(BlogPost)
admin.site.register(CommentModel)
admin.site.register(CommentOfComment)
