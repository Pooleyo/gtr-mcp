import pytest

from logging import getLogger

logger = getLogger(__name__)

from app.client import GtrClient

class TestGtrClient():

    @pytest.mark.asyncio
    async def test_gtr_client_project(self):
        projects = await GtrClient.get_projects(q="ashley")

