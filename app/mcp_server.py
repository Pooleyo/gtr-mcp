from mcp.server.fastmcp import FastMCP

from app.client import GtrClient

mcp = FastMCP("gtr")


@mcp.tool()
async def get_projects(q: str):
    """Get projects from the GtR API that match a query.
    
    Args:
        q: A very query that is used to detect matching keywords in the title, abstract or project reference.
    """
    projects = await GtrClient.get_projects(q)
    return projects

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()