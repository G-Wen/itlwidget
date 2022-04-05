import json
import requests

key_map = {
    "entrant_id": "id",
    "members_name": "name",
    "entrant_ranking_points": "ranking_points",
    "entrant_total_song_points": "song_points",
    "entrant_total_bonus_points": "bonus_points",
    "entrant_total_songs_pass": "passes",
    "entrant_total_songs_fc": "full_combos",
    "entrant_total_songs_fec": "full_excellent_combos",
    "entrant_total_songs_quad": "quad_stars",
    "entrant_total_songs_quint": "quint_stars",
    "entrant_rank": "rank",
}

def get_entrant(entrant_id):
    r = requests.get(f"<GrooveStats API Endpoint")
    itl_ladder = json.loads(r.text)
    self = ""
    entrant = {}
    rivals = []
    ladder = []
    for entry in itl_ladder["data"]["entrants"]:
        player = {}
        for itl_key in key_map:
            player[key_map[itl_key]] = entry[itl_key]
        player["total_points"] = player["song_points"] + player["bonus_points"]

        if entry["entrant_is_self"]:
            player["name"]
            player["type"] = "self"
            entrant = player.copy()
        elif entry["entrant_is_rival"]:
            rivals.append(player["name"])
            player["type"] = "rival"
        else:
            player["type"] = "neutral"
        
        ladder.append(player)

    for i in range(3):
        entrant[f"rival{i+1}"] = None
    for i, rival in enumerate(rivals):
        entrant[f"rival{i+1}"] = rival

    entrant['ladder'] = ladder
    for ladder_entry in ladder:
        ladder_entry['difference'] = entrant['ranking_points'] - ladder_entry['ranking_points']

    return entrant