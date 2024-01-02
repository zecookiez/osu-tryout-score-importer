class StatsScore:
    def __init__(self, score, beatmap_id):
        self.source = score
        self.accuracy = score.accuracy
        self.score_value = score.score
        self.mods = str(score.mods)
        self.beatmap_id = beatmap_id
        self.player_id = score.user_id
        self.results_include = True
