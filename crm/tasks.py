from celery import shared_task
from datetime import datetime
import requests
import os

@shared_task
def generate_crm_report():
    # Example GraphQL query (adapt schema fields if different in your project)
    query = """
    query {
        allCustomers { totalCount }
        allOrders { totalCount, totalAmount }
    }
    """

    # Call local GraphQL API (assuming it runs on localhost:8000/graphql)
    response = requests.post(
        "http://localhost:8000/graphql/",
        json={'query': query}
    )
    data = response.json().get("data", {})

    total_customers = data.get("allCustomers", {}).get("totalCount", 0)
    total_orders = data.get("allOrders", {}).get("totalCount", 0)
    total_revenue = data.get("allOrders", {}).get("totalAmount", 0)

    # Build report string
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

    # Log to /tmp/crm_report_log.txt
    log_file = "/tmp/crm_report_log.txt"
    with open(log_file, "a") as f:
        f.write(report)

    return report
