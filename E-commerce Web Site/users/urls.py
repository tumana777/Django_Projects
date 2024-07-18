from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, profile
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, 
                                       PasswordResetConfirmView, PasswordResetCompleteView, 
                                       PasswordChangeView, PasswordChangeDoneView)

urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="register"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/logout/", UserLogoutView.as_view(), name="logout"),
    path("user/password_reset/", PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path("user/password_reset/done/", PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path("user/password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path("user/password_reset_complete/", PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path("user/profile/", profile, name="profile"),
    path("user/password_change/", PasswordChangeView.as_view(template_name='users/password_change.html/'), name="password_change"),
    path("user/password_change/done/", PasswordChangeDoneView.as_view(template_name='users/password_change_done.html/'), name="password_change_done"),
]