import os

from espn_api.basketball import League


def league_from_env():

    return League(
        league_id=int(os.environ.get("LEAGUE_ID", "0")),
        year=int(os.environ.get("LEAGUE_YEAR", "0")),
        espn_s2=os.environ.get("LEAGUE_ESPN_S2"),
        swid=os.environ.get("LEAGUE_SWID"),
    )
