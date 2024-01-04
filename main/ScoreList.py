from collections import defaultdict
from StatsScore import StatsScore


class ScoreList:
    def __init__(self, scores: list[StatsScore]):
        self.player_scores = defaultdict(list)
        self.source = scores
        self.name_map = {}
        for score in scores:
            self.add_score(score)

    def add_score(self, score: StatsScore):
        """
        Overwrites score if beatmap id, player id, and mods match
        """
        for ind, player_score in enumerate(self.player_scores[score.player_id]):
            if player_score.beatmap_id != score.beatmap_id:
                continue
            if player_score.mods == score.mods:
                self.player_scores[score.player_id][ind] = score
                break
        else:
            self.player_scores[score.player_id].append(score)
        return self

    def get_players(self):
        return list(self.player_scores.keys())

    def update_name_map(self, api):
        players = api.users(self.get_players())
        self.name_map = {
            player.id: player.username for player in players
        }
        return self

    def get_beatmap_scores(self):
        beatmap_scores = defaultdict(list)  # <beatmap id, StatsScore>
        for player, scores in self.player_scores.items():
            for score in scores:
                beatmap_scores[score.beatmap_id].append(score)
        for scores in beatmap_scores.values():
            scores.sort(key=lambda i: i.normalized, reverse=True)
        return beatmap_scores

    def drop_bottom_scores(self, k=1):
        for player, scores in self.player_scores.items():
            scores.sort(key=lambda i: i.normalized, reverse=True)
            # Mark score as do not include
            for ind in range(1, k + 1):
                scores[-ind].results_include = False
        return self
