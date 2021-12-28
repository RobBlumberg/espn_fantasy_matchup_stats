from bs4 import BeautifulSoup
import requests


def get_schedule(day: str):
    """
    Return NBA matchups on queried date.
    """

    day = day.replace("-", "")
    url = f"https://www.espn.com/nba/schedule/_/date/{day}"

    response = requests.get(url)
    bs = BeautifulSoup(response.text)

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
                teams.append(team.span.text)
            except AttributeError:
                pass

        all_games.append(teams)

    return all_games
