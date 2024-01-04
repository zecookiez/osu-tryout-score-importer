from collections import defaultdict
from ossapi import Ossapi, MatchEventType
from re import findall
from ScoreList import ScoreList
from StatsScore import StatsScore
from write_scores import store_player_score, store_leaderboard_score


def load_scores(matches):
    scores = []
    for match in matches:
        for event in match.events:
            if event.detail.type != MatchEventType.OTHER:
                continue
            for score in event.game.scores:
                scores.append(StatsScore(score, event.game.beatmap_id))
    return scores


def main():
    # see sample_secrets.txt to format your secrets.txt file
    with open("secrets.txt", "r") as file:
        attributes = {}
        for line in file.readlines():
            key, val = line.strip().split("=")
            attributes[key] = val
        client_id = int(attributes["client_id"])
        client_secret = attributes["client_secret"]
        api = Ossapi(client_id, client_secret)

    # read mp ids requested
    mp_ids = set()
    with open("mp_ids.txt", "r") as mp_input:
        for line in mp_input.readlines():
            mp_ids.add(int(findall(r"\d+", line)[0]))
    score_list = ScoreList(load_scores([api.match(id) for id in mp_ids])).update_name_map(api).drop_bottom_scores(3)

    # print scores per beatmap
    for beatmap_id, scores in score_list.get_beatmap_scores().items():
        print(beatmap_id)
        for score in scores:
            if not score.results_include:
                print("[EXCLUDED] ", end="")
            print(score_list.name_map[score.player_id], score.score_value, score.normalized, "%.2f" % score.accuracy, score.mods)

    # write scores to a json file (will restore this info later)
    store_player_score(score_list)
    store_leaderboard_score(score_list)


if __name__ == "__main__":
    main()
