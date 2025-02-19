import threading

_thread_locals = threading.local()


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store current user and IP in thread locals
        _thread_locals.current_user = (
            request.user if request.user.is_authenticated else None
        )
        _thread_locals.current_ip = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)

        # Clean up thread locals
        if hasattr(_thread_locals, 'current_user'):
            del _thread_locals.current_user
        if hasattr(_thread_locals, 'current_ip'):
            del _thread_locals.current_ip

        return response
