from collections import defaultdict
from json import load

def main():
    # avg score - every player's average score across the pool
    data = {}
    with open("output/player_scores.json", "r", encoding="utf-8") as file:
        data = load(file)
    if "players" not in data:
        return
    players = data["players"]
    results = []
    for id, scores in players.items():
        tot_score = sum(score["normalized"] for score in scores["scores"] if score["results_include"])
        maps_played = sum(score["results_include"] for score in scores["scores"])
        avg_score = tot_score / maps_played
        results.append({
            "id": id,
            "username": scores["username"],
            "maps played": maps_played,
            "total": tot_score,
            "avg": avg_score
        })
    results.sort(key = lambda i: i["avg"], reverse=True)
    for rank, player in enumerate(results, 1):
        print(rank, player["username"], player["avg"])



if __name__ == "__main__":
    main()
