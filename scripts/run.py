from asyncio import BaseTransport
import os
from socket import timeout
import time
from typing import Any

from dotenv import load_dotenv

from python_graphql_client_example.transport.request import RequestTransport
from python_graphql_client_example.client.sync_client import SyncGraphQLClient
from python_graphql_client_example.queries.repository import repository_issues_query

load_dotenv()  # take environment variables from .env

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_GRAPHQL_ENDPOINT = os.environ.get("GITHUB_GRAPHQL_ENDPOINT")

def main():
    transport = RequestTransport(
        endpoint=GITHUB_GRAPHQL_ENDPOINT, token=GITHUB_TOKEN, # type: ignore
    )
   
    
    with SyncGraphQLClient(transport=transport) as client: # type: ignore
        data = client.execute_sync(
            query=repository_issues_query, variables={},
        )
        print(data)
    
    transport.close()

if __name__ == "__main__":
    main()