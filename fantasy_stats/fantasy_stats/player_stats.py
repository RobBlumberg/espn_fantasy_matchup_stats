import pandas as pd


def get_player_stats(team):
    """
    team : espn_api Team object
    """
    stats_df = pd.DataFrame(
        {player.name: player.stats["002021"]["avg"] for player in team.roster}
    ).T

    stats_total = stats_df.sum()
    stats_total["FG%"] = stats_total["FGM"] / stats_total["FGA"]
    stats_total["FT%"] = stats_total["FTM"] / stats_total["FTA"]

    keep_stats = ["PTS", "BLK", "STL", "FG%", "FT%", "REB", "AST", "3PTM", "TO"]

    return stats_total[keep_stats]


def matchup_comparison(team1, team2):

    stats_team1 = get_player_stats(team1)
    stats_team2 = get_player_stats(team2)

    match_stats = pd.merge(
        stats_team1.to_frame(),
        stats_team2.to_frame(),
        left_index=True,
        right_index=True,
    )
    match_stats.columns = [team1.team_name, team2.team_name]

    return match_stats
