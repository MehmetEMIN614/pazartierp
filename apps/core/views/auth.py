from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from apps.core.utils.throttles import BurstRateThrottle, CustomUserThrottle


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [BurstRateThrottle]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        token = AccessToken.for_user(user)

        return Response({
            'access_token': str(token),
            'user_id': user.id,
            'username': user.username
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserThrottle]

    def post(self, request):
        # With JWT, server-side logout isn't necessary
        # The client should just remove the token
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
