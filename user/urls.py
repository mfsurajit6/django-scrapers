from django.urls import path
from user.views import CustomLoginView, RegistrationView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout')
]
