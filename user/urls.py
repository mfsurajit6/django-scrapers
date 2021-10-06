from django.urls import path
from user.views import CustomLoginView, RegistrationView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),

    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(),
        name="reset_password"
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_done.html'),
        name="password_reset_complete"
    ),
]
