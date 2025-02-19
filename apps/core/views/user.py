from rest_framework.response import Response
from rest_framework.decorators import action
from apps.core.models.user import User
from apps.core.views.base import BaseModelViewSet

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    filterset_fields = ['role', 'is_active']
    ordering_fields = ['email', 'created_at']

    def get_queryset(self):
        """Only show users from current organization"""
        return super().get_queryset().filter(orgs=self.request.user.current_org)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
