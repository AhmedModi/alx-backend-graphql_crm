#!/bin/bash
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DELETED_COUNT=$(python3 manage.py shell -c "from datetime import timedelta; from django.utils import timezone; from crm.models import Customer; cutoff = timezone.now() - timedelta(days=365); qs = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff); count = qs.count(); qs.delete(); print(count)")
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
