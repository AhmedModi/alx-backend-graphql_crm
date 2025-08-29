#!/bin/bash
# Script to delete inactive customers (no orders in past 1 year)
# Logs results to /tmp/customer_cleanup_log.txt

LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Run Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

# Log the result with timestamp
echo \"[\$TIMESTAMP] Deleted \$DELETED_COUNT inactive customers\" >> \$LOG_FILE
