# GTR MCP - Gateway to Research API Client

A Python client for interacting with the UK Research and Innovation (UKRI) Gateway to Research (GTR) API. This client provides easy access to research project data, including project information, funding details, and associated persons and organisations.

## Features

- Search for research projects by keyword
- Retrieve specific projects by ID
- Get projects associated with specific persons or organisations
- Flexible query parameters (pagination, sorting, field selection)
- Simple and intuitive API
- Context manager support for resource management

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone <repository-url>
cd gtr-mcp

# Install dependencies
uv sync
```

## Quick Start

### Basic Usage

```python
from app.gtr_client import GtrClient

# Create a client
with GtrClient() as client:
    # Get top 10 results for a query
    results = client.get_top_results("machine learning", limit=10)

    for project in results:
        print(f"Title: {project['title']}")
        print(f"ID: {project['id']}")
```

### Run the Example Script

The repository includes an example script that demonstrates how to search for projects:

```bash
# Run with default query ("machine learning")
uv run python scripts/example_search.py

# Run with custom query
uv run python scripts/example_search.py "artificial intelligence"
uv run python scripts/example_search.py quantum computing
```

## API Methods

### `search_projects(query, page=1, page_size=10, search_fields=None, sort_field=None, sort_order='D')`

Search for projects using a keyword query.

**Parameters:**
- `query` (str): Search term to query
- `page` (int): Page number, starting at 1 (default: 1)
- `page_size` (int): Number of results per page, between 10 and 100 (default: 10)
- `search_fields` (list): List of field codes to search in
- `sort_field` (str): Field code to sort by
- `sort_order` (str): Sort order - 'A' for ascending or 'D' for descending

**Example:**
```python
results = client.search_projects(
    query="climate change",
    page=1,
    page_size=20,
    search_fields=["pro.t", "pro.a"],  # Search in title and abstract
    sort_field="pro.am",  # Sort by funded value
    sort_order="D"  # Descending
)
```

### `get_project(project_id)`

Retrieve a specific project by ID.

**Example:**
```python
project = client.get_project("966CDC25-3993-4B58-A78A-54EDA6C06555")
```

### `get_person_projects(person_id, page=1, page_size=10)`

Retrieve all projects for a specific person.

**Example:**
```python
projects = client.get_person_projects("6E91436D-44FA-4F53-BF0E-AEADAA93906C")
```

### `get_organisation_projects(organisation_id, page=1, page_size=10)`

Retrieve all projects for a specific organisation.

**Example:**
```python
projects = client.get_organisation_projects("012CC3C1-34E8-44D9-A932-1060CF647F7B")
```

### `get_top_results(query, limit=10, search_fields=None)`

Convenience method to get the top N results for a query.

**Example:**
```python
top_projects = client.get_top_results("neuroscience", limit=5)
```

## Available Search Fields

- `pro.gr`: Project Reference
- `pro.t`: Project Title
- `pro.a`: Project Abstract
- `pro.orcidId`: ORCID iD
- `pro.rt`: Research Topics
- `pro.ha`: Health Activities
- `pro.rcukp`: RCUK Programmes
- `pro.lf`: Lead Funder Name

## Available Sort Fields

- `pro.sd`: Start Date
- `pro.ed`: End Date
- `pro.am`: Funded Value
- `score`: Relevance (default for searches)

## Project Structure

```
gtr-mcp/
├── app/
│   └── gtr_client/
│       ├── __init__.py
│       └── GtrClient.py       # Main client class
├── scripts/
│   └── example_search.py      # Example usage script
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## API Access Note

**Important:** The GTR API at `gtr.ukri.org` may have access restrictions or firewall rules that prevent direct access from certain networks or IP addresses. If you encounter 403 Forbidden errors, this may be due to:

1. Network firewall restrictions
2. API access policies requiring specific headers or authentication
3. IP-based access control

If you experience connectivity issues, you may need to:
- Check your network configuration
- Contact UKRI for API access requirements
- Use the API from an allowed network/IP address

## Development

### Running Tests

```bash
# TODO: Add tests
uv run pytest
```

### Code Structure

The client is designed with:
- Type hints for better IDE support
- Comprehensive docstrings
- Error handling with proper exception raising
- Context manager support for resource cleanup

## License

See LICENSE file for details.

## References

- [GTR API Documentation](http://gtr.ukri.org/resources/api.html)
- [UKRI Official Website](https://www.ukri.org/)
