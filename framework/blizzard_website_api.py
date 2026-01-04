import asyncio

import logging
import requests
from framework.utils import get_season_id

logger = logging.getLogger(__name__)

class BlizzardWebsiteAPI:
    def __init__(self,
        locale="fr_FR",
        url="https://hearthstone.blizzard.com/fr-fr/api/community",
        proxies=None
        ):
        if proxies is None:
            proxies = {}

        self.session = requests.Session()
        self.session.proxies = proxies

        self.locale = locale
        self.url = url

    async def get_leaderboard_data(self,
        page=1,
        leaderboardId="standard",
        region="EU"
        ):
        seasonId=get_season_id()
        url = f"{self.url}/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page={page}&seasonId={seasonId}"
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Erreur on {url}: {response.status_code}")
        except Exception as e:
            logger.error(e)
        return None
