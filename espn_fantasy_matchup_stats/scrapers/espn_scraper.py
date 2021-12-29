from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np

from typing import Union


FANTASY_NAME_TO_SCHEDULE_MAPPER = {
    "Atlanta": "ATL",
    "Boston": "BOS",
    "Brooklyn": "BKN",
    "Charlotte": "CHA",
    "Chicago": "CHI",
    "Cleveland": "CLE",
    "Dallas": "DAL",
    "Denver": "DEN",
    "Detroit": "DET",
    "Golden State": "GSW",
    "Houston": "HOU",
    "Indiana": "IND",
    "LA": "LAC",
    "Los Angeles": "LAL",
    "Memphis": "MEM",
    "Miami": "MIA",
    "Milwaukee": "MIL",
    "Minnesota": "MIN",
    "New Orleans": "NOP",
    "New York": "NYK",
    "Oklahoma City": "OKC",
    "Orlando": "ORL",
    "Philadelphia": "PHL",
    "Phoenix": "PHO",
    "Portland": "POR",
    "Sacramento": "SAC",
    "San Antonio": "SAS",
    "Toronto": "TOR",
    "Utah": "UTA",
    "Washington": "WAS",
}


def get_schedule(day: str, format_: Union[pd.DataFrame, set] = set):
    """
    Return NBA matchups on queried date.

    Arguments:
    ----------
    day: str
        Date for which to get schedule.
        Format  = YYYY-MM-DD
    format_: Union[pd.DataFrame, set] (default=set)
        Must be either pd.DataFrame or set.
    """
    msg = "format_ must be either 'pd.DataFrame' or 'set'."
    assert format_ in {pd.DataFrame, set}, msg

    day = day.replace("-", "")
    url = f"https://www.espn.com/nba/schedule/_/date/{day}"

    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")

    # find matchup schedule tables
    matchup_table = bs.find(
        name="table", attrs={"class": "schedule has-team-logos align-left"}
    )

    # parse through table and pull out all matchups
    all_games = []
    for tr in matchup_table.find_all("tr", {"class": ["odd", "even"]}):

        teams = []
        for td in tr.find_all("td"):
            team = td.find("a", {"class": "team-name"})

            try:
                teams.append(FANTASY_NAME_TO_SCHEDULE_MAPPER[team.span.text])
            except AttributeError:
                pass

        all_games.append(teams)

    # sleep to avoid too many requests
    if format_ == pd.DataFrame:
        return pd.DataFrame(all_games)
    elif format_ == set:
        return set(np.array(all_games).flatten())
