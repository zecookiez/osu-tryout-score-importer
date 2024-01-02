from collections import defaultdict
from json import dump
from ScoreList import ScoreList
from StatsScore import StatsScore

def store_player_score(score_list):
    data = {}
    for player_id, scores in score_list.player_scores.items():
        data[player_id] = {
            "username": score_list.name_map[player_id],
            "scores": [],
        }
        for score in scores:
            data[player_id]["scores"].append(dict(vars(score)))
            data[player_id]["scores"][-1].pop("source")
            data[player_id]["scores"][-1].pop("player_id")
    data = {"players": data}
    with open("output/player_scores.json", "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=2)

def store_leaderboard_score(score_list):
    data = {}
    for beatmap_id, scores in score_list.get_beatmap_scores().items():
        data[beatmap_id] = []
        for rank, score in enumerate(scores, 1):
            data[beatmap_id].append(dict(vars(score)))
            data[beatmap_id][-1]["rank"] = str(rank)
            data[beatmap_id][-1]["username"] = score_list.name_map[score.player_id]
            data[beatmap_id][-1].pop("source")
            data[beatmap_id][-1].pop("beatmap_id")
    data = {"beatmaps": data}
    with open("output/beatmap_scores.json", "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=2)