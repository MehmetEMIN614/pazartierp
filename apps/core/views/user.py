from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.core.models import User, Org
from apps.core.serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    filterset_fields = ['is_active', 'role']
    ordering_fields = ['email', 'created_at']

    def get_queryset(self):
        """Only return users from current organization"""
        return self.queryset.filter(orgs=self.request.user.current_org)

    def perform_create(self, serializer):
        """Add user to current organization"""
        user = serializer.save()
        user.orgs.add(self.request.user.current_org)
        return user

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password')
        if not password:
            return Response(
                {'error': 'Password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(password)
        user.save()
        return Response({'status': 'password changed'})
