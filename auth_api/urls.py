from django.urls import path
from auth_api.views import (
    SignUpView,
    SignInView,
    UserInfoView,
    LatencyView,
    LogoutView
)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('info/', UserInfoView.as_view(), name='info'),
    path('latency/', LatencyView.as_view(), name='latency'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
