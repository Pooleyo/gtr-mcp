from mcp.server.fastmcp import FastMCP

from app.client import GtrClient

mcp = FastMCP("gtr")


@mcp.tool()
async def get_projects(q: str):
    """Get projects from the GtR API matching a query
    
    Args:
        q: A very short query that is used to detect matching keywords in the title, abstract or project reference.
    """
    response = await GtrClient.get_projects(q)
    return response.json()

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()