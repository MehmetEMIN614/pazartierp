from django.urls import path

from apps.core.views.auth import LoginView
from apps.core.views.user import UserViewSet

urlpatterns = [
    # Auth
    path('login', LoginView.as_view(), name='login'),

    # User
    path('users/<int:pk>', UserViewSet.as_view({'get': 'retrieve'})),
]
