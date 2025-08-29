from __future__ import absolute_import, unicode_literals
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    {
      allCustomers {
        totalCount
      }
      allOrders {
        totalCount
        totalRevenue
      }
    }
    """)

    result = client.execute(query)

    customers = result.get("allCustomers", {}).get("totalCount", 0)
    orders = result.get("allOrders", {}).get("totalCount", 0)
    revenue = result.get("allOrders", {}).get("totalRevenue", 0)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_line)

    return log_line
