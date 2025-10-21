#!/usr/bin/env python3
"""Example script demonstrating how to use the GTR Client to search for projects."""
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the app module
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.gtr_client import GtrClient


def format_project(project: dict, index: int) -> str:
    """Format a project dictionary for display.

    Args:
        project: Project dictionary from the API
        index: Index number for display

    Returns:
        Formatted string representation of the project
    """
    title = project.get("title", "N/A")
    project_id = project.get("id", "N/A")
    abstract = project.get("abstractText", "N/A")

    # Truncate abstract if too long
    if len(abstract) > 200:
        abstract = abstract[:200] + "..."

    # Get funding information
    fund = project.get("fund", {})
    if isinstance(fund, dict):
        amount = fund.get("valuePounds", "N/A")
        start = fund.get("start", "N/A")
        end = fund.get("end", "N/A")
    else:
        amount = "N/A"
        start = "N/A"
        end = "N/A"

    output = f"\n{'=' * 80}\n"
    output += f"Result #{index}\n"
    output += f"{'=' * 80}\n"
    output += f"Title: {title}\n"
    output += f"ID: {project_id}\n"
    output += f"Funding: £{amount:,}" if isinstance(amount, (int, float)) else f"Funding: {amount}\n"
    output += f"Period: {start} to {end}\n"
    output += f"\nAbstract:\n{abstract}\n"

    return output


def main():
    """Main function to demonstrate GTR client usage."""
    # Default search query
    query = "machine learning"

    # Check if a custom query was provided
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

    print(f"\n🔍 Searching GTR for: '{query}'")
    print(f"{'=' * 80}\n")

    try:
        # Create the client using context manager
        with GtrClient(timeout=30.0) as client:
            # Get top 10 results
            print("Fetching top 10 results...")
            results = client.get_top_results(query=query, limit=10)

            if not results:
                print(f"\n❌ No results found for query: '{query}'")
                return

            print(f"\n✅ Found {len(results)} result(s)\n")

            # Display each result
            for idx, project in enumerate(results, 1):
                print(format_project(project, idx))

            print(f"\n{'=' * 80}")
            print(f"Displaying {len(results)} of top results")
            print(f"{'=' * 80}\n")

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
