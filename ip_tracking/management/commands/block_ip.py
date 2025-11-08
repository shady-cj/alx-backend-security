
from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIPs

class IPManagementCommand(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--ip',
            type=str,
            help='Ip Address to block',
        )
    def handle(self, *args, **options):
        ip = options["ip"]
        _, created = BlockedIPs.objects.get_or_create(ip_address=ip)
        if created:
            self.stdout.write(f"{ip} blocked successfully")
        else:
            self.stdout.write(f"{ip} already in block list")

