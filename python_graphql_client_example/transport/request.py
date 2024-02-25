from typing import Any, Optional

import requests as r
from python_graphql_client_example.transport.base import BaseTransport

class RequestTransport(BaseTransport):
    """The transport based on requests library."""

    session: Optional[r.Session]

    def __init__(self, endpoint: str, token: str, **kwargs: Any) -> None:
        self.endpoint = endpoint
        self.token = token
        self.auth_header = {"Authorization": f"Bearer {self.token}"}
        self.session = None

    def connect(self) -> None:
        """Start a 'requests.Session connection."""
        if self.session is None:
            self.session = r.Session()
        else:
            raise Exception("Session already started.")
        
    def close(self) -> None:
        """Close a 'requests.Session connection."""
        if self.session is not None:
            self.session.close()
            self.session = None

    def execute(self, query: str, variables: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Execute the query."""
        if self.session is None:
            raise Exception("RequestTransport session not active.")
        
        post_args = {
            "headers": self.auth_header,
            "json": {"query": query, "variables": variables},
        }
        post_args["headers"]["Content-type"] = "application/json"

        response = self.session.request("POST", self.endpoint, **post_args)
        result = response.json()
        return result.get("data")

    