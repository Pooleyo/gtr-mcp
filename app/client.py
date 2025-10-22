import httpx
from logging import getLogger

from app.schemas import Project

logger = getLogger(__name__)

class GtrClient():
    USER_AGENT = "gtr-mcp-server/0.0.1"
    GTR_API_BASE = "https://gtr.ukri.org/gtr/api/"
    GTR_API_PROJECTS = f"{GTR_API_BASE}/projects"

    @staticmethod
    async def get_projects(q: str) -> list[Project]:
        """Make a request to the GtR API projects endpoint"""
        url = f"{GtrClient.GTR_API_PROJECTS}/?{q=}"
        headers = {
            "User-Agent": GtrClient.USER_AGENT,
            "Accept": "application/json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            body = response.json()
            project_list = body["project"]
            ### For investigating the keys in the response
            # keys_present = {}
            # for p in project_list:

            #     for k in p.keys():
            #         if k not in keys_present.keys():
            #             keys_present[k] = 1
            #         else: 
            #             keys_present[k] += 1
            # logger.error(f"{keys_present=}")
            return [
                Project(
                    title=p["title"],
                    abstractText=p["abstractText"],
                    techAbstractText=p.get("techAbstractText", None),
                    potentialImpact=p.get("potentialImpact", None),
                ) 
                for p in project_list 
                if p.get("title") and p.get("abstractText")
            ]
