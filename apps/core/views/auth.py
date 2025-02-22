from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        # Check if org_id is provided
        if not request.data.get('org_id'):
            return Response({
                'error': 'Organization ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        response = super().post(request, *args, **kwargs)

        # Get user from email after successful authentication
        user = User.objects.get(email=request.data.get('email'))

        # Check if user has any organizations
        if not user.orgs.exists():
            return Response({
                'error': 'User has no organization access'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            org = user.orgs.get(id=request.data['org_id'], active=True)
        except:
            return Response({
                'error': 'Invalid organization ID',
                'available_orgs': user.orgs.filter(active=True).values('id', 'name')
            }, status=status.HTTP_400_BAD_REQUEST)

        # Set current organization
        user.set_current_org(org)

        return Response({
            'access_token': response.data['access'],
            'current_org': {
                'id': org.id,
                'name': org.name
            },
            'available_orgs': user.orgs.filter(active=True).values('id', 'name')
        })
