![](https://github.com/RobBlumberg/espn_fantasy_matchup_stats/workflows/build/badge.svg)

# ESPN Fantasy Stats Package

Python package to pull fantasy matchup stats using the [espn api](https://github.com/cwendt94/espn-api) and predict the outcome of the weekly matchup.

## Usage

### Authenticating

Your league `SWID` and `ESPN_S2` values can be found by right clicking anywhere within your espn fantasy league, and selecting `Inspect`. Select `Application` on the top bar, then click on `https://fantasy.espn.com/` under `Storage`, `Cookies`. A table will show up, where you should be able to find your `SWID` and `ESPN_S2`. For more details, see [here](https://github.com/cwendt94/espn-api/wiki).

Once you have these values, export them into your environment.
```
export LEAGUE_SWID = <your_league_swid>
export LEAGUE_ESPN_S2 = <your_league_espn_s2>
export LEAGUE_ID = <your_league_id>
export LEAGUE_YEAR = 2021 | 2020 | 2019
```

### Getting your weekly matchup stats prediction
```python
from espn_api.basketball import League
from espn_fantasy_matchup_stats.auth import Auth
from espn_fantasy_matchup_stats.player_stats import matchup_comparison

# Authenticate
auth = Auth()

# League object
league = League(
    league_id=auth.LEAGUE_ID,
    year=auth.LEAGUE_YEAR,
    espn_s2=auth.LEAGUE_ESPN_S2,
    swid=auth.LEAGUE_SWID,
)

# Find my team and opponent's team
my_team_name = "<your_team_name>"
my_team = next((x for x in league.teams if x.team_name == my_team_name), None)
matchup = my_team.schedule[-1]
opp_team = (
    matchup.home_team
    if matchup.home_team.team_name != my_team_name
    else matchup.away_team
)

# Get stats
comparison = matchup_comparison(my_team, opp_team)
print(comparison)
```
```
           My Team      Opp Team
PTS     235.503350    207.420880
BLK       6.392811      7.484106
STL      11.360628     13.731366
FG%       0.470374      0.441689
FT%       0.772200      0.768535
REB      77.858028     81.014537
AST      49.572522     55.806319
3PTM     28.338662     24.505562
TO       27.614537     27.989369
```