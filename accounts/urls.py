from django.urls import path
from accounts import views
# Register,
from accounts.views import ( Profile, DeleteProfile, UserLoginView, UserLogoutView, ProfileView, PasswordChange)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name='accounts'

urlpatterns=[
    # Login and Logout
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('profile/', login_required(Profile.as_view()), name='profile'),
    # <int:pk>/
    # path('register/', Register.as_view(), name='register'),
    path('register/', views.register, name='register'),
    
    path('edit-profile/', login_required(ProfileView.as_view()), name='edit_profile'),

    path('delete-profile/', login_required(DeleteProfile.as_view()), name='delete_profile'),

    path('delete-profile-image', login_required(views.delete_profile_picture) , name='delete_profile_picture'),

    path('change-password/', login_required(PasswordChange.as_view()), name='change_password'),

    #ACTIVATE ACCOUNT
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    #RECOVER PASSWORD
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),

] 
    # <int:pk>/