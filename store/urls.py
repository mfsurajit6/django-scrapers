from django.urls import path
from store.views import IndexView, SendEmail


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('send_email/', SendEmail.as_view(), name='send_email'),
]
