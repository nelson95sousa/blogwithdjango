from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from blog.models import BlogPost
from blog.models import CommentModel, CommentOfComment
from blog.forms import BlogPostForm, CommentForm, CommentOfCommentForm, ApprovePostCommentsForm, ApproveComentCommentsForm
from django.views.generic import View, FormView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.http import HttpResponseForbidden
# Create your views here.

class Index(ListView):
    model = BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return BlogPost.objects.filter(date__lte=timezone.now()).order_by('-date')


# ///////////////////////////////////////////////////////////////////////////////////////

from django.views import View
# POST+COMMENT+COMMENTofCOMMENT VIEW
class PostView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get("form_type")=='cmt-pst':
            view = CommentView.as_view()
            return view(request, *args, **kwargs)
        elif request.method == 'POST' and request.POST.get("form_type")=='cmt-cmt':
            view = CommentOfCommentView.as_view()
            return view(request, *args, **kwargs)

# POST DETAIL VIEW
class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post.html'
    context_object_name = 'blogpost'
    success_url = reverse_lazy('blog:post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['form_reply'] = CommentOfCommentForm
        return context
from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin
#CREATE POST COMMENTS
class CommentView(CreateView):
    model = CommentModel
    form_class = CommentForm
    success_message= 'Your comment was created successfully! It is waiting approval'

    def get_success_url(self):
        return reverse('blog:post', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get("form_type")=='cmt-pst':
            comment_post_form = CommentForm(request.POST)
            comment_post_form.instance.user = request.user
            comment_post_form.instance.blogPost = BlogPost.objects.get(id=self.kwargs['pk'])
            if comment_post_form.is_valid():
                messages.success(self.request, 'Your comment was submited successfully and is now waiting for approval!')
                comment_post_form.save()
            return super().form_valid(comment_post_form)
        else:
            comment_post_form = CommentForm(request.POST, prefix='cmt-pst')
            
#CREATE COMMENTS OF COMMENTS
class CommentOfCommentView(CreateView):
    model = CommentOfComment
    form_class = CommentOfCommentForm

    def get_success_url(self):
        return reverse('blog:post', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get("form_type")=='cmt-cmt':
            comment_comment_form = CommentOfCommentForm(request.POST)
            comment_comment_form.instance.user = request.user
            comment_comment_form.instance.comment = CommentModel.objects.get(id=request.POST.get("comment_id"))
            comment_comment_form.instance.blogPost = BlogPost.objects.get(id=request.POST.get("post_id"))
            # print(request.POST.get("comment_id") )
            # print( comment_comment_form.instance.blogPost)
            if comment_comment_form.is_valid():
                messages.success(self.request, 'Your comment was submited successfully and is now waiting for approval!')
                comment_comment_form.save()
            return super().form_valid(comment_comment_form)
        else:
            comment_comment_form = CommentOfCommentForm(request.POST, prefix='cmt-cmt')
      
# ///////////////////////////////////////////////////////////////////////////////////
# APPROVE COMMENTS LIST
class PostComments(PermissionRequiredMixin,ListView):
    model = BlogPost
    template_name = 'blog/post_comments.html'
    context_object_name = 'blogpost'
    success_url = reverse_lazy('blog:post_comments')
    permission_required = 'is_staff'

    

#PAGE TO APPROVE COMMENTS(DETAIL+ 2 FORMS)
class PostCommentsView(PermissionRequiredMixin,View):
    permission_required = 'is_staff'
    def get(self, request, *args, **kwargs):
        view = ApproveComments.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get("form_type")=='cmt-pst':
            view = CommentApproveView.as_view()
            return view(request, *args, **kwargs)
        elif request.method == 'POST' and request.POST.get("form_type")=='cmt-cmt':
            view = CommentOfCommentApproveView.as_view()
            return view(request, *args, **kwargs)

#POST DETAIL TO APPROVE COMMENTS
class ApproveComments(PermissionRequiredMixin,DetailView):
    model = BlogPost
    template_name = 'blog/approve_comments.html'
    context_object_name = 'blogpost'
    success_url = reverse_lazy('blog:approve_comments')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApprovePostCommentsForm
        context['form_reply'] = ApproveComentCommentsForm
        #comments to the post not approved:
        context['cmts_not_approved'] = CommentModel.objects.select_related('blogPost').filter(approved_comment=False, blogPost_id=self.get_object())
        #comments of comments not approved:
        context['cmts_cmts_not_approved'] = CommentOfComment.objects.select_related('blogPost').filter(approved_comment=False, blogPost_id=self.get_object())
        return context


#POST COMMENTS
class CommentApproveView(PermissionRequiredMixin, UpdateView):
    model = CommentModel
    form_class = ApprovePostCommentsForm
    permission_required = 'is_staff'

    def get_success_url(self):
        return reverse('blog:approve_comments', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get("form_type")=='cmt-pst':
            comment = get_object_or_404(CommentModel, pk=request.POST.get("comment_pk"))
            comment.approve()
            return redirect('blog:approve_comments', pk=comment.blogPost.pk)
            
#COMMENTS OF COMMENTS
class CommentOfCommentApproveView(PermissionRequiredMixin,UpdateView):
    model = CommentOfComment
    form_class = ApproveComentCommentsForm
    permission_required = 'is_staff'

    def get_success_url(self):
        return reverse('blog:approve_comments', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get("form_type")=='cmt-cmt':
            comment = get_object_or_404(CommentOfComment, pk=request.POST.get("comment_pk"))
            comment.approve()
            return redirect('blog:approve_comments', pk=comment.blogPost.pk)

    # /////////////////

class DeleteCommentPost(PermissionRequiredMixin,DeleteView):
        
    permission_required = 'is_staff'
    model= CommentModel
    context_object_name = 'comment'
    template_name = "blog/delete_comment_post.html"
    
    def get_object(self):
        return get_object_or_404(CommentModel, pk= self.kwargs['pk'] )
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:approve_comments', kwargs={'pk':self.object.blogPost.pk})

class DeleteCommentComment(PermissionRequiredMixin,DeleteView):
        #user is same userthat created the comment or staff - HOW TO DO IT???
    permission_required = 'is_staff'
    model= CommentOfComment
    context_object_name = 'comment'
    template_name = "blog/delete_comment_comment.html"
    
    def get_object(self):
        return get_object_or_404(CommentOfComment, pk= self.kwargs['pk'] )
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:approve_comments', kwargs={'pk':self.object.blogPost.pk})
    

# ///////////////////////////////////////////////////////////////////////////////////

class CreatePost(PermissionRequiredMixin,CreateView):
    permission_required = 'is_staff'
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:index')

class DeletePost(PermissionRequiredMixin,DeleteView):
    permission_required = 'is_staff'
    model= BlogPost
    context_object_name = 'post'
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy('blog:index')
    def get_object(self):
        return get_object_or_404(BlogPost, pk= self.kwargs['pk'] )


class EditPost(PermissionRequiredMixin,UpdateView):
    permission_required = 'is_staff'

    model = BlogPost
    
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/edit_post.html'
    
    context_object_name = 'post'
    
    def get_object(self):
        return get_object_or_404(BlogPost, pk= self.kwargs['pk'] )