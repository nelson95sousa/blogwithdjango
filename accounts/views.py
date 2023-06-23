from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from accounts.forms import RegisterForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import redirect

from accounts.forms import SetPasswordUserForm


# Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            
            return redirect('accounts:login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(
        request=request,
        template_name="accounts/register.html",
        context={"form": form}
        )

# Login View
class UserLoginView(LoginView): 
    template_name='accounts/login.html'

    def dispatch(self, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().dispatch(*args, **kwargs)


# Logout View        
class UserLogoutView(LogoutView):
    login_url = None


#Profile View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Profile(TemplateView):
    template_name = 'accounts/profile.html'
    @method_decorator(login_required)
    def get_object(self, request,id):
        if request.user.id == id:
            return get_object_or_404(User, user=request.user)
        else :
            raise Http404

    # context_object_name = 'user.id'


# Edit Profile View
class ProfileView(UpdateView):
    model = User
    
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/edit_profile.html'
    
    context_object_name = 'user.id'
    
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

#Delete Profile View
class DeleteProfile(DeleteView):
    model= User
    context_object_name = 'user.id'
    success_url = '/'
    template_name = "accounts/delete_profile.html"
    success_url = reverse_lazy('main:index')
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

#Delete profile picture view
def delete_profile_picture(self):
    self.user.profile_pic.delete(save=True)
    return redirect('accounts:edit_profile')

#Change Password
class PasswordChange(PasswordChangeView):
    model = User
    context_object_name = 'user.id'
    form_class = SetPasswordUserForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/password_reset_confirm.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)




# EMAIL STUFF
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

def activateEmail(request, user, to_email):
    mail_subject = 'Blog With Django - activate your user account'
    message = render_to_string('accounts/activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <strong>{user.first_name}</strong> <strong>{user.last_name}</strong>, please go to your email <strong>{to_email}</strong> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.', extra_tags='safe')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.', extra_tags='safe')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for confirm your email, now you can login.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('accounts:login')

# RECOVER PASSWORD
from accounts.forms import PasswordResetForm

from .forms import PasswordResetForm
from django.db.models.query_utils import Q


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Blog With Django - Password Reset request"
                message = render_to_string("accounts/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[user_email])
                if email.send():
                    messages.success(request,
                        """
                        <h5>Password reset sent</h5>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('accounts:login')


    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="accounts/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordUserForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('accounts:login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordUserForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("accounts:login")