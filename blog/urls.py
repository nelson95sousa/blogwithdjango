from django.urls import path
from blog.views import Index, PostView, CreatePost, DeletePost, EditPost, PostComments, PostCommentsView, DeleteCommentPost, DeleteCommentComment
# , CommentOfCommentView
from django.contrib.auth.decorators import login_required

app_name='blog'

urlpatterns=[
    path('', Index.as_view(),name='index'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('create_post/', login_required(CreatePost.as_view()), name='create_post'),
    path('<int:pk>/delete_post/', login_required(DeletePost.as_view()), name='delete_post'),
    path('edit_post/<int:pk>/', login_required(EditPost.as_view()), name='edit_post'),
    #Comments
    path('post-comments/', login_required(PostComments.as_view()), name='post_comments'),
    path('approve-comments/<int:pk>/', login_required(PostCommentsView.as_view()), name='approve_comments'),
    path('<int:pk>/delete_comment_post/', login_required(DeleteCommentPost.as_view()), name='delete_comment_post'),
    path('<int:pk>/delete_comment_comment/', login_required(DeleteCommentComment.as_view()), name='delete_comment_comment'),
]

