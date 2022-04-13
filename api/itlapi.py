import json
import requests
from gsendpoints import *
import time
from collections import Counter

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
    r = requests.get(f"{streamer_stats_endpoint}{entrant_id}")
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

def get_score_info(entrant_id):
    entrant_scores = json.loads(requests.get(f"{entrant_scores_endpoint}{entrant_id}").text)['songScores']
    entrant_scores = {score["song_id"]: score for score in entrant_scores if score["score_ex"]}
    return entrant_scores

def get_matchup_info(songlist1, songlist2):
    mutual_songs = set(songlist1).intersection(set(songlist2))
    vs_info = []
    for song_id in mutual_songs:
        p1_score = songlist1[song_id]
        p2_score = songlist2[song_id]
        info = {}
        info['song_id'] = song_id
        info['song_title'] = p1_score['song_title']
        info['song_artist'] = p1_score['song_artist']
        info['song_points'] = p1_score['song_points']
        info['song_meter'] = p1_score['song_meter']
        info['p1_score_ex'] = p1_score['score_ex']
        info['p1_score_points'] = p1_score['score_points']
        info['p1_score_bonus_points'] = p1_score['score_bonus_points']
        info['p1_score_best_clear_type'] = p1_score['score_best_clear_type']
        info['p2_score_ex'] = p2_score['score_ex']
        info['p2_score_points'] = p2_score['score_points']
        info['p2_score_bonus_points'] = p2_score['score_bonus_points']
        info['p2_score_best_clear_type'] = p2_score['score_best_clear_type']
        info['score_ex_difference'] = p1_score['score_ex'] - p2_score['score_ex']
        info['score_points_difference'] = p1_score['score_points'] - p2_score['score_points']
        vs_info.append(info)

    vs_info.sort(key=lambda x: x['score_ex_difference'])
    """
    mu_info = {}
    p1_clears = Counter(x['p1_score_best_clear_type'] for x in vs_info)
    p2_clears = Counter(x['p2_score_best_clear_type'] for x in vs_info)
    print(p1_clears)
    print(p2_clears)
    """
    return vs_info

async def get_versus_info(entrant_id, rivals):
    if not rivals:
        return []

    entrant_scores = get_score_info(entrant_id)
    time.sleep(0.2)
    
    rivals_scores = []
    for rival_id in rivals:
        rival_scores = get_score_info(rival_id)
        time.sleep(0.2)
        rivals_scores.append(rival_scores)

    vs_info = [get_matchup_info(entrant_scores, rival_scores) for rival_scores in rivals_scores]
    return vs_info
    