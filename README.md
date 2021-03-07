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

### Instantiate MyTeam object
```python
from espn_fantasy_matchup_stats.auth import my_league
from espn_fantasy_matchup_stats.my_team import MyTeam

# Instatiate MyTeam object
my_team_name = "<your_team_name>"
my_team = MyTeam(my_league, my_team_name)
```

### Useful methods
Below is a brief overview of some useful methods. For comprehensive documentation, see [docs](TBD).
- TODO



