from blog.models import BlogPost, CommentModel, CommentOfComment
from accounts.models import User
from django.db import models
from django import forms
from django.forms import ModelForm
from ckeditor_uploader.fields import RichTextUploadingField


class BlogPostForm(ModelForm):

    text = RichTextUploadingField()

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'label',
            'text',
            'post_image',
            'date',
            ]



from django.utils import timezone

class CommentForm(ModelForm):  

    created_date = models.DateTimeField(default=timezone.now)    
    comment = forms.CharField(
        widget= forms.TextInput(attrs={'placeholder':' write a comment...'}),
        )

    class Meta:
        model = CommentModel
        fields = [
            'comment',
            ]

class CommentOfCommentForm(ModelForm):  

    created_date = models.DateTimeField(default=timezone.now)    
    text = forms.CharField(
        widget= forms.TextInput(attrs={'placeholder':' write a comment...'}),
        )

    class Meta:
        model = CommentOfComment
        fields = [
            'text',
            ]

class ApprovePostCommentsForm(ModelForm):   
   
    class Meta:
        model = CommentModel
        fields = (
            'approved_comment',
        )


class ApproveComentCommentsForm(ModelForm):
     class Meta:
        model = CommentOfComment
        fields = (
            'approved_comment',
        )
