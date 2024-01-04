from collections import defaultdict
from json import load

def main():
    # avg percent - take the percentage of each score from the top score per map, then average across the pool
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
        highest = None
        for score in included:
            if not highest:
                highest = score
            players[score["player_id"]].append((score["normalized"] / highest["normalized"], score))
    for id, percents in players.items():
        tot_percent = sum(percent for percent, _ in percents)
        maps_played = len(percents)
        avg_percent = tot_percent / maps_played
        results.append({
            "id": id,
            "username": percents[0][1]["username"],
            "maps played": maps_played,
            "total": tot_percent,
            "avg": avg_percent
        })
    results.sort(key = lambda i: i["avg"], reverse=True)
    for rank, player in enumerate(results, 1):
        print(rank, player["username"], player["avg"])



if __name__ == "__main__":
    main()
