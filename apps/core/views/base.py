from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for models inheriting from BaseModel.
    Handles organization-specific data and user tracking.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset by user's current organization"""
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'current_org'):
            return queryset.filter(org=self.request.user.current_org)
        return queryset.none()

    def perform_create(self, serializer):
        """Add user and organization information"""
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            org=self.request.user.current_org
        )

    def perform_update(self, serializer):
        """Update the updated_by field"""
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive instead of delete"""
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response({'status': 'archived'})
