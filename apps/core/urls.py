from django.urls import path

from apps.core.views.auth import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
