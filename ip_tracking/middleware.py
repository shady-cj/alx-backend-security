from .models import RequestLog, BlockedIPs
from django.http import HttpResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.datetime.now()
        user = request.user
        path = request.path
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # Take the first IP in the list
        else:
            ip = request.META.get("REMOTE_ADDR")
        
        RequestLog.objects.create(ip_address=ip, timestamp=now, path=path)
        is_blocked = BlockedIPs.objects.get(ip_address=ip)
        if is_blocked:
            return HttpResponse('IP blocked from making request', status=403)
        response = self.get_response(request)
        

        return response