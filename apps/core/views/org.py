from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.serializers.org import OrgSerializer


class OrgViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrgSerializer

    def get_queryset(self):
        return self.request.user.orgs.filter(active=True)

    @action(detail=True, methods=['post'])
    def switch(self, request, pk=None):
        try:
            org = self.get_object()
            request.user.set_current_org(org)

            return Response({
                'message': 'Organization switched successfully',
                'current_org': {
                    'id': org.id,
                    'name': org.name
                }
            })
        except:
            return Response({
                'error': 'Failed to switch organization'
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'organizations': serializer.data,
            'current_org': {
                'id': request.user.current_org.id,
                'name': request.user.current_org.name
            } if request.user.current_org else None
        })
