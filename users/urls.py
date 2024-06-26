from django.urls import path
from users.views import RegisterUserAPIView, FetchUserDetailsAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register-user'),
    path('my-profile/', FetchUserDetailsAPIView.as_view(), name='my-profile'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
