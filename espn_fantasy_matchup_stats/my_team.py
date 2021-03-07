import pandas as pd


class MyTeam:
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

    def get_player_stats(self, total=False):
        """
        Determines expected value per game for an espn fantasy team
        for the following stats:
        ["PTS", "BLK", "STL", "FG%", "FT%", "REB", "AST", "3PTM", "TO"]

        Returns:
        --------
        pd.DataFrame
        """
        stats_df = pd.DataFrame(
            {player.name: player.stats["002021"]["avg"] for player in self.team.roster}
        ).T

        keep_cols = ["PTS", "BLK", "STL", "FG%", "FT%", "REB", "AST", "3PTM", "TO"]

        if not total:
            return stats_df[keep_cols]
        else:
            stats_total = stats_df.sum()
            stats_total["FG%"] = stats_total["FGM"] / stats_total["FGA"]
            stats_total["FT%"] = stats_total["FTM"] / stats_total["FTA"]

            return stats_total[keep_cols]

    def get_current_matchup_comparison(self):
        """
        Compares the expected values per game for my espn fantasy team
        and my opponent's team for the current matchup.
        Compared stats are:
        ["PTS", "BLK", "STL", "FG%", "FT%", "REB", "AST", "3PTM", "TO"]

        Returns:
        --------
        pd.DataFrame
        """
        stats_my_team = self.get_player_stats(total=True)

        opp_team = self.get_opponents_team()
        stats_opp_team = opp_team.get_player_stats(total=True)

        match_stats = pd.merge(
            stats_my_team.to_frame(),
            stats_opp_team.to_frame(),
            left_index=True,
            right_index=True,
        )
        match_stats.columns = [self.team.team_name, opp_team.team.team_name]

        return match_stats
