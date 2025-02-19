from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import PermissionDenied

from apps.core.models.org import Org


class CurrentOrgMiddleware(MiddlewareMixin):
    """Middleware to handle organization context for API requests"""

    def process_request(self, request):
        if not request.user.is_authenticated:
            return None

        # Get org_id from header or query params
        org_id = (
                request.headers.get('X-Organization-ID') or
                request.query_params.get('org_id')
        )

        if org_id and str(org_id).isdigit():
            try:
                org = request.user.orgs.get(id=org_id, active=True)
                request.user.set_current_org(org)
            except Org.DoesNotExist:
                raise PermissionDenied("Invalid organization ID")

        # Ensure user has a current organization
        if not request.user.get_current_org():
            raise PermissionDenied("No organization context")

        # Add current org to request
        request.org = request.user.current_org
