from rest_framework.throttling import (
    UserRateThrottle,
    ScopedRateThrottle,
    SimpleRateThrottle
)

# 1. Basic User/Anon Throttles
class CustomUserThrottle(UserRateThrottle):
    rate = '50/hour'
    scope = 'custom'

# 2. Burst and Sustained Throttles
class BurstRateThrottle(UserRateThrottle):
    rate = '5/minute'
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    rate = '100/day'
    scope = 'sustained'

# 3. Custom IP-Based Throttle
class IPRateThrottle(SimpleRateThrottle):
    rate = '5/minute'
    scope = 'ip'

    def get_cache_key(self, request, view):
        ident = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

# 4. Scoped API Throttle
class ScopedAPIThrottle(ScopedRateThrottle):
    scope_attr = 'throttle_scope'  # This matches with the throttle_scope attribute in views
