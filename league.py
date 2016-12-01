#!/usr/bin/env python
# -*- coding: utf-8 -*-

import external
from bot_functions import BotFunctions


class LeagueOfLegends(object):
    @staticmethod
    def url_with_api_key(url):
        if external.data.credentials["riotApiKey"] is None:
            raise ValueError("Riot development API key is not set")

        return url + "?api_key=" + external.data.credentials["riotApiKey"]

    @staticmethod
    async def get_summoner_id(summoner_name):
        """
        Return the summoner id for the given summoner name

        :param summoner_name: the summoner name (as a string)
        :returns:   the summoner id of the given summoner name
                    or `None` if the summoner id couldn't be found
        """

        json_url = LeagueOfLegends.url_with_api_key("https://eune.api.pvp.net/api/lol/eune/v1.4/summoner/by-name/" +
                                                    summoner_name)

        json_data = BotFunctions.get_remote_json_contents(json_url)
        if json_data is not None:
            if summoner_name.lower() in json_data:
                return str(json_data[summoner_name.lower()]["id"])

        return None

    @staticmethod
    async def get_rune_pages(summoner_id):
        """
        Return a list with the names of the rune pages for the given summoner

        :param summoner_id: the summoner id (as a string)
        :returns: a list with the names of the rune pages
        """

        json_url = LeagueOfLegends.url_with_api_key("https://eune.api.pvp.net/api/lol/eune/v1.4/summoner/" +
                                                    summoner_id + "/runes")

        json_data = BotFunctions.get_remote_json_contents(json_url)
        if json_data is not None:
            if summoner_id in json_data:
                return [page["name"] for page in json_data[summoner_id]["pages"]]

        return None

    @staticmethod
    async def get_tier(summoner_id):
        """
        Return the tier of the given summoner

        :param summoner_id: the summoner id (as a string)
        :returns: the tier (e.g. "SILVER") of the given summoner
        """

        json_url = LeagueOfLegends.url_with_api_key("https://eune.api.pvp.net/api/lol/eune/v2.5/league/by-summoner/" +
                                                    summoner_id + "/entry")

        json_data = BotFunctions.get_remote_json_contents(json_url)
        if json_data is not None:
            if summoner_id in json_data:
                for league in json_data[summoner_id]:
                    if league["queue"] == "RANKED_SOLO_5x5":
                        return league["tier"]

        return None
