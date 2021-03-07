class MyTeam:
    def __init__(self, league, team_name):
        assert team_name in [x.team_name for x in league]
        self.league = league
        self.team = next((x for x in league.teams if x.team_name == team_name), None)

    def get_opponents_team(self):
        matchup = self.team.schedule[-1]
        return (
            matchup.home_team
            if matchup.home_team.team_name != self.team_name
            else matchup.away_team
        )
