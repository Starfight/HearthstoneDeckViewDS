import asyncio

import requests
from framework.utils import get_season_id

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
        region="EU",
        seasonId=get_season_id()
        ):
        url = f"{self.url}/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page={page}&seasonId={seasonId}"
        response = self.session.get(url)
        return response.json()
