#!/usr/bin/env python3
import sys
import asyncio
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

query = gql("""
    query GetRecentOrders($cutoff: DateTime!) {
        orders(orderDate_Gte: $cutoff) {
            id
            customer {
                email
            }
        }
    }
""")

async def fetch_orders():
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
    result = await client.execute_async(query, variable_values={"cutoff": cutoff_date})
    return result.get("orders", [])

async def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    orders = await fetch_orders()
    with open(LOG_FILE, "a") as f:
        for order in orders:
            order_id = order.get("id")
            email = order.get("customer", {}).get("email")
            f.write(f"[{timestamp}] Order {order_id} reminder sent to {email}\n")
    print("Order reminders processed!")

if __name__ == "__main__":
    asyncio.run(main())
