class StatsScore:
    mod_multiplier = {
        "DT": 1.2,
        "HR": 1.1,
        "HD": 1.06,
        "FL": 1.12,
        "EZ": 0.5,
    }
    def __init__(self, score, beatmap_id):
        self.source = score
        self.accuracy = score.accuracy
        self.score_value = self.normalized = score.score
        self.mods = str(score.mods)
        self.beatmap_id = beatmap_id
        self.player_id = score.user_id
        self.results_include = True
        # Calculate normalized score
        for mod, mult in StatsScore.mod_multiplier.items():
            if mod in self.mods:
                self.normalized /= mult
