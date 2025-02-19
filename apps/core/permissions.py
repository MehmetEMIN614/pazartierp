from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils.translation import gettext_lazy as _
from apps.core.utils.constants import UserRole


class BaseRolePermission(BasePermission):
    """Base permission class for role checking"""
    allowed_roles = []
    message = _('Insufficient permissions.')

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role in self.allowed_roles
        )


class IsAdmin(BaseRolePermission):
    allowed_roles = [UserRole.ADMIN]
    message = _('Admin access required.')


class IsAccountManager(BaseRolePermission):
    allowed_roles = [UserRole.ACCOUNT_MANAGER]
    message = _('Account manager access required.')


class IsStaff(BaseRolePermission):
    allowed_roles = [UserRole.STAFF]
    message = _('Staff access required.')


class IsUser(BaseRolePermission):
    allowed_roles = [UserRole.USER]
    message = _('User access required.')


# Role combination classes
class IsAdminOrAccountManager(BaseRolePermission):
    allowed_roles = [UserRole.ADMIN, UserRole.ACCOUNT_MANAGER]
    message = _('Admin or account manager access required.')


class IsAdminOrStaff(BaseRolePermission):
    allowed_roles = [UserRole.ADMIN, UserRole.STAFF]
    message = _('Admin or staff access required.')


class IsStaffOrAccountManager(BaseRolePermission):
    allowed_roles = [UserRole.STAFF, UserRole.ACCOUNT_MANAGER]
    message = _('Staff or account manager access required.')


class HasOrganizationContext(BasePermission):
    """
    Permission class to ensure user has organization context
    """
    message = _('No organization context set.')

    def has_permission(self, request, view):
        return bool(request.user and request.user.get_current_org())


class IsOwner(BasePermission):
    """Permission class to check if user is owner of the object"""
    message = _('You must be the owner of this object.')

    def has_object_permission(self, request, view, obj):
        return bool(
            hasattr(obj, 'created_by') and obj.created_by == request.user or
            hasattr(obj, 'user') and obj.user == request.user
        )


class ReadOnly(BasePermission):
    """Permission class to only allow read-only actions"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsActiveUser(BasePermission):
    """Permission class to check if user is active"""
    message = _('Your account is not active.')

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)


class HasOrgPermission(BasePermission):
    """
    Permission class to check if user has specific permission in current org
    Usage: HasOrgPermission('invoices.create_invoice')
    """
    def __init__(self, perm_name):
        self.perm_name = perm_name
        self.message = _(f'You do not have {perm_name} permission in this organization.')

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.has_org_perm(self.perm_name, request.org)
        )


class IsAdminOrReadOnly(BasePermission):
    """Permission class to allow read-only access to all users but write access only to admins"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == UserRole.ADMIN
        )


class IsOwnerOrReadOnly(BasePermission):
    """Permission class to allow read-only access to all users but write access only to owners"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
            
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class HasRequiredFields(BasePermission):
    """
    Permission class to check if request data contains required fields
    Usage: HasRequiredFields(['field1', 'field2'])
    """
    def __init__(self, required_fields):
        self.required_fields = required_fields
        self.message = _('Missing required fields.')

    def has_permission(self, request, view):
        if request.method not in ['POST', 'PUT', 'PATCH']:
            return True
            
        return all(field in request.data for field in self.required_fields)


#