import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
from datetime import timedelta
from functools import reduce

from espn_fantasy_matchup_stats.scrapers.espn_scraper import get_schedule


class MyTeam:

    _KEEP_STATS = [
        "PTS",
        "BLK",
        "STL",
        "FGM",
        "FGA",
        "FG%",
        "FTM",
        "FTA",
        "FT%",
        "REB",
        "AST",
        "3PTM",
        "TO",
    ]

    def __init__(self, league, team_name):
        assert team_name in [
            x.team_name for x in league.teams
        ], f"{team_name} is not a team in this league."
        self.league = league
        self.team = next((x for x in league.teams if x.team_name == team_name), None)

    def get_opponents_team(self):
        """
        Returns MyTeam object for current opponent's team.
        """
        matchup = self.team.schedule[-1]
        opp_team = (
            matchup.home_team
            if matchup.home_team.team_name != self.team.team_name
            else matchup.away_team
        )
        return MyTeam(self.league, opp_team.team_name)

    def get_injury_status(self):
        """
        Returns injury status for entire roster.
        """

        return {
            self.team.roster[i].name: self.team.roster[i].injuryStatus
            for i in range(len(self.team.roster))
        }

    def daily_player_matches(self, game_date):
        # TODO: make game_date datetime.date

        s = get_schedule(game_date)

        return {player.name: player.proTeam in s for player in self.team.roster}

    def get_player_stats(self, stat_type: str = "total"):
        """
        Returns player average stats using the specified stat_type.

        Arguments:
        ----------
        stat_type : str (default="total")
            Time window for which to get player stats.
            Must be one of:
            {"total", "last_7", "last_15", "last_30", "projected_total"}


        Returns:
        --------
        pd.DataFrame
        """
        stats_dict = {}
        missing_players = []
        for player in self.team.roster:
            try:
                stats_dict[player.name] = player.stats[
                    f"{stat_type}_{self.league.year}"
                ]["avg"]
            except KeyError:
                missing_players.append(player.name)

        stats_df = pd.DataFrame(stats_dict)

        for player in missing_players:
            stats_df[player] = np.zeros(22)

        return stats_df.T[MyTeam._KEEP_STATS]

    def get_daily_projected_stats(self, game_date, stat_type: str = "total"):
        """
        Returns projected player stats for queried date by checking injury status.
        Projections are estimated using the specified stat_type.
        """
        # TODO: make game_date datetime.date

        date_now = datetime.date(datetime.now())
        game_datetime = date.fromisoformat(game_date)

        days_diff = np.abs((date_now - game_datetime).days)

        # if queried game_date is more than 1 day from now, DTD player is considered ACTIVE
        injury_status = self.get_injury_status()
        if days_diff > 1:
            for key in injury_status:
                injury_status[key] = (
                    "ACTIVE"
                    if injury_status[key] == "DAY_TO_DAY"
                    else injury_status[key]
                )

        stats_df = self.get_player_stats(stat_type=stat_type)
        stats_df["injury_status"] = stats_df.index.map(injury_status)

        # map daily schedule to player stats
        schedule = self.daily_player_matches(game_date)
        stats_df["has_game"] = stats_df.index.map(schedule)

        # if injury_status is not ACTIVE or player does not have game, set all projected stats to 0
        for idx, row in stats_df.iterrows():
            if row["injury_status"] != "ACTIVE" or not row["has_game"]:
                stats_df.loc[idx, "PTS":"TO"] = np.zeros(stats_df.shape[1] - 2)

        return stats_df

    def get_matchup_comparison(
        self, start_date: date, end_date: date, stat_type: str = "total"
    ):
        """
        Compares the projected stats between team and current opponent for the specified date range,
        using the specified stat_type.

        Returns:
        --------
        pd.DataFrame
        """
        daily_comparisons = []
        for game_date in [
            start_date + timedelta(i) for i in range((end_date - start_date).days + 1)
        ]:

            stats_my_team = self.get_daily_projected_stats(
                str(game_date), stat_type=stat_type
            )
            opp_team = self.get_opponents_team()
            stats_opp_team = opp_team.get_daily_projected_stats(
                str(game_date), stat_type=stat_type
            )

            team_stats_sum_list = []
            for team_stats in [stats_my_team, stats_opp_team]:
                team_stats_sum = team_stats.sum()
                team_stats_sum_list.append(team_stats_sum)

            match_stats = pd.concat(team_stats_sum_list, axis=1)
            match_stats.columns = [self.team.team_name, opp_team.team.team_name]

            match_stats.drop("injury_status")

            daily_comparisons.append(match_stats)

        dfs_agg = reduce(lambda x, y: x.add(y, fill_value=0), daily_comparisons)
        dfs_agg.loc["FG%"] = dfs_agg.loc["FGM"] / dfs_agg.loc["FGA"]
        dfs_agg.loc["FT%"] = dfs_agg.loc["FTM"] / dfs_agg.loc["FTA"]

        return dfs_agg.drop(["injury_status", "has_game"])
