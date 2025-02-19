from rest_framework.response import Response
from rest_framework.decorators import action
from apps.core.models.org import Org
from apps.core.views.base import BaseModelViewSet


class OrgViewSet(BaseModelViewSet):
    queryset = Org.objects.all()
    search_fields = ['name', 'address']
    filterset_fields = ['active']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['post'])
    def switch_organization(self, request, pk=None):
        org = self.get_object()
        request.user.set_current_org(org)
        return Response({'status': 'switched organization'})
