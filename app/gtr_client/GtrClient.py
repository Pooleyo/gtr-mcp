"""GTR API Client for querying UK Research and Innovation Gateway to Research data."""
from typing import Optional, Dict, List, Any
import httpx


class GtrClient:
    """Client for interacting with the Gateway to Research (GTR) API.

    The GTR API provides access to UK Research and Innovation data including
    projects, persons, organisations, and more.
    """

    BASE_URL = "http://gtr.ukri.org/gtr/api"

    def __init__(self, timeout: float = 30.0):
        """Initialize the GTR client.

        Args:
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the client."""
        self.close()

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def search_projects(
        self,
        query: str,
        page: int = 1,
        page_size: int = 10,
        search_fields: Optional[List[str]] = None,
        sort_field: Optional[str] = None,
        sort_order: str = "D"
    ) -> Dict[str, Any]:
        """Search for projects using a keyword query.

        Args:
            query: Search term to query
            page: Page number, starting at 1 (default: 1)
            page_size: Number of results per page, between 10 and 100 (default: 10)
            search_fields: List of field codes to search in (e.g., ['pro.t', 'pro.a'])
                         If None, searches default fields (title, abstract, reference, orcid)
            sort_field: Field code to sort by (e.g., 'pro.sd' for start date, 'score' for relevance)
            sort_order: Sort order - 'A' for ascending or 'D' for descending (default: 'D')

        Returns:
            Dictionary containing the API response with project data

        Available search fields:
            - pro.gr: Project Reference
            - pro.t: Project Title
            - pro.a: Project Abstract
            - pro.orcidId: ORCID iD
            - pro.rt: Research Topics
            - pro.ha: Health Activities
            - pro.rcukp: RCUK Programmes
            - pro.lf: Lead Funder Name

        Available sort fields:
            - pro.sd: Start Date
            - pro.ed: End Date
            - pro.am: Funded Value
            - score: Relevance
        """
        # Validate page size
        if page_size < 10 or page_size > 100:
            raise ValueError("page_size must be between 10 and 100")

        # Validate sort order
        if sort_order not in ["A", "D"]:
            raise ValueError("sort_order must be 'A' (ascending) or 'D' (descending)")

        # Build query parameters
        params = {
            "q": query,
            "p": page,
            "s": page_size,
        }

        # Add search fields if specified
        if search_fields:
            params["f"] = search_fields

        # Add sort parameters if specified
        if sort_field:
            params["sf"] = sort_field
            params["so"] = sort_order

        # Make the request
        url = f"{self.BASE_URL}/projects"
        response = self.client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Retrieve a specific project by ID.

        Args:
            project_id: The unique identifier for the project

        Returns:
            Dictionary containing the project data
        """
        url = f"{self.BASE_URL}/projects/{project_id}"
        response = self.client.get(url)
        response.raise_for_status()

        return response.json()

    def get_person_projects(
        self,
        person_id: str,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Retrieve all projects for a specific person.

        Args:
            person_id: The unique identifier for the person
            page: Page number, starting at 1 (default: 1)
            page_size: Number of results per page (default: 10)

        Returns:
            Dictionary containing the API response with project data
        """
        url = f"{self.BASE_URL}/persons/{person_id}/projects"
        params = {"p": page, "s": page_size}
        response = self.client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_organisation_projects(
        self,
        organisation_id: str,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Retrieve all projects for a specific organisation.

        Args:
            organisation_id: The unique identifier for the organisation
            page: Page number, starting at 1 (default: 1)
            page_size: Number of results per page (default: 10)

        Returns:
            Dictionary containing the API response with project data
        """
        url = f"{self.BASE_URL}/organisations/{organisation_id}/projects"
        params = {"p": page, "s": page_size}
        response = self.client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_top_results(
        self,
        query: str,
        limit: int = 10,
        search_fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get the top N results for a query.

        This is a convenience method that searches for projects and returns
        just the project items (not the full API response structure).

        Args:
            query: Search term to query
            limit: Number of top results to return (default: 10)
            search_fields: List of field codes to search in (default: None, searches all default fields)

        Returns:
            List of project dictionaries (top results)
        """
        # Calculate page size (max 100)
        page_size = min(limit, 100)

        # Search with relevance sorting
        response = self.search_projects(
            query=query,
            page=1,
            page_size=page_size,
            search_fields=search_fields,
            sort_field="score",
            sort_order="D"
        )

        # Extract projects from response
        # The API returns data in a nested structure
        projects = []
        if "project" in response:
            # If there's a single project, it might be a dict
            if isinstance(response["project"], dict):
                projects = [response["project"]]
            # If there are multiple projects, it will be a list
            elif isinstance(response["project"], list):
                projects = response["project"]

        # Return only the requested number of results
        return projects[:limit]
