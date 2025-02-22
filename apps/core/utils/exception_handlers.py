# apps/core/utils/exceptions.py
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST framework that handles additional exceptions.
    """
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(exc.messages)

    if isinstance(exc, Http404):
        exc = NotFound()

    if isinstance(exc, IntegrityError):
        exc = APIException(_('Database integrity error occurred.'))

    response = exception_handler(exc, context)

    # If unexpected error occurs (500)
    if response is None:
        return Response({
            'success': False,
            'message': _('An unexpected error occurred.'),
            'detail': str(exc) if str(exc) else _('Internal server error'),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    error_response = {
        'success': False,
        'message': _('An error occurred.'),
        'code': response.status_code,
    }

    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            error_response['errors'] = {}
            for field, value in exc.detail.items():
                if isinstance(value, (list, dict)):
                    error_response['errors'][field] = value
                else:
                    error_response['errors'][field] = [str(value)]
        elif isinstance(exc.detail, list):
            error_response['errors'] = exc.detail
        else:
            error_response['errors'] = [str(exc.detail)]

    # Add request information for debugging
    if hasattr(context, 'get') and context.get('request'):
        error_response['path'] = context['request'].path
        error_response['method'] = context['request'].method

    response.data = error_response
    return response


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad request.')
    default_code = 'bad_request'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Resource not found.')
    default_code = 'not_found'


class Forbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'forbidden'


class UnauthorizedAccess(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided or are invalid.')
    default_code = 'unauthorized'


class InvalidInput(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _('Invalid input.')
    default_code = 'invalid_input'


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Resource conflict.')
    default_code = 'conflict'
