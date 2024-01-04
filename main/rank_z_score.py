from collections import defaultdict
from json import load

def main():
    # z sum - for every beatmap, get the z score of each player's score, then sum them all up
    data = {}
    with open("output/beatmap_scores.json", "r", encoding="utf-8") as file:
        data = load(file)
    if "beatmaps" not in data:
        return
    beatmaps = data["beatmaps"]
    players = defaultdict(list)
    results = []
    for id, scores in beatmaps.items():
        included = [*filter(lambda i: i["results_include"], scores)]
        if len(included) <= 1:
            continue
        total_score = sum(score["normalized"] for score in included)
        N = len(included)
        mean = total_score / N
        sigma = sum(pow(score["normalized"] - mean, 2) / N for score in included)
        stddev = pow(sigma, 0.5)
        for score in included:
            players[score["player_id"]].append((max(0, score["normalized"] - mean) / stddev, score))
    for id, z_scores in players.items():
        tot_z = sum(z for z, _ in z_scores)
        maps_played = len(z_scores)
        avg_z = tot_z / maps_played
        results.append({
            "id": id,
            "username": z_scores[0][1]["username"],
            "maps played": maps_played,
            "total": tot_z,
            "avg": avg_z
        })
    results.sort(key = lambda i: i["avg"], reverse=True)
    for rank, player in enumerate(results, 1):
        print(rank, player["username"], player["avg"])



if __name__ == "__main__":
    main()
