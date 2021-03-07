import os
from espn_api.basketball import League


class Auth:
    """
    Class to hold espn_api creds.
    """

    def __init__(self):
        self.LEAGUE_SWID = os.environ.get("LEAGUE_SWID")
        self.LEAGUE_ESPN_S2 = os.environ.get("LEAGUE_ESPN_S2")
        self.LEAGUE_ID = int(os.environ.get("LEAGUE_ID", "0"))
        self.LEAGUE_YEAR = int(os.environ.get("LEAGUE_YEAR", "0"))

auth=Auth()

my_league = League(
    league_id=auth.LEAGUE_ID,
    year=auth.LEAGUE_YEAR,
    espn_s2=auth.LEAGUE_ESPN_S2,
    swid=auth.LEAGUE_SWID,
)
