from auth import Auth
from player_stats import get_player_stats, matchup_comparison

from espn_api.basketball import League
import pandas as pd

league = League(
    league_id=Auth().LEAGUE_ID,
    year=Auth().LEAGUE_YEAR,
    espn_s2=Auth().LEAGUE_ESPN_S2, 
    swid=Auth().LEAGUE_SWID
)

my_team = [t for t in league.teams if t.team_name == "Drip Bayless"][0]
matchup_teams = [my_team.schedule[-1].home_team, my_team.schedule[-1].away_team]
opp_team = matchup_teams[0] if matchup_teams[0].team_name != "Drip Bayless" else matchup_teams[1]

match_stats = matchup_comparison(my_team, opp_team)