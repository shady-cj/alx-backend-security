from celery import shared_task
from .models import SuspiciousIP,RequestLog
from datetime import timedelta, datetime
from django.db.models import Count

@shared_task
def check_for_suspicious_ips():
    hour_ago = datetime.now() - timedelta(hours=1)
    logs_from_an_hour_ago = RequestLog.objects.filter(timestamp__gte=hour_ago)
    ips_with_more_than_100_logs = logs_from_an_hour_ago.values("ip_address").annotate(ip_occurence=Count('ip_address')).filter(ip_occurence__gte=100)
    # for log in ips_with_more_than_100_logs:
    #     SuspiciousIP.objects.create(ip_address=ip, reason=reason)
    for log in ips_with_more_than_100_logs:
        SuspiciousIP.objects.create(ip_address=log.get('ip_address'), reason=f"ip requested {log.get('ip_occurence')} times")

    ips_with_sensitive_paths = logs_from_an_hour_ago.filter(path__in=["login/", "admin/", "protected/"]).values("ip_address", "path").distinct()
    for ip in ips_with_sensitive_paths:
        SuspiciousIP.objects.create(ip_address=ip.get('ip_address'), reason=f"ip accessed {ip.get('path')}")



