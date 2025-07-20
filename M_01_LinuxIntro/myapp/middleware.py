import time
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests

class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = 5  # время в секундах между запросами с одного IP

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip:
            last_request = cache.get(ip)
            now = time.time()
            if last_request and now - last_request < self.timeout:
                return HttpResponseTooManyRequests("Слишком много запросов — попробуйте чуть позже.")
            cache.set(ip, now, timeout=self.timeout)
        response = self.get_response(request)
        return response