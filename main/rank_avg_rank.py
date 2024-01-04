from collections import defaultdict
from json import load

def main():
    # avg rank - rank player's score per beatmap, then take the average across the pool
    data = {}
    with open("output/beatmap_scores.json", "r", encoding="utf-8") as file:
        data = load(file)
    if "beatmaps" not in data:
        return
    beatmaps = data["beatmaps"]
    players = defaultdict(list)
    results = []
    for id, scores in beatmaps.items():
        included = filter(lambda i: i["results_include"], scores)
        for rank, score in enumerate(included, 1):
            players[score["player_id"]].append((rank, score))
    for id, ranks in players.items():
        tot_rank = sum(rank for rank, _ in ranks)
        maps_played = len(ranks)
        avg_rank = tot_rank / maps_played
        results.append({
            "id": id,
            "username": ranks[0][1]["username"],
            "maps played": maps_played,
            "total": tot_rank,
            "avg": avg_rank
        })
    results.sort(key = lambda i: i["avg"])
    for rank, player in enumerate(results, 1):
        print(rank, player["username"], player["avg"])



if __name__ == "__main__":
    main()
