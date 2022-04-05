# Do not use this to run the api, it is included for historical purposes
# It is slow and inefficient and only existed as temporary solution
# until groovestats made an api to provide the data directly.

from requests_html import AsyncHTMLSession

session = AsyncHTMLSession()

async def get_leaderboard():
    r = await session.get('https://itl2022.groovestats.com/leaderboard')
    await r.html.arender(wait=1, sleep=1)
    result = r.html.text.split('\n')[9:-5]
    leaderboard = []
    for i in range(0, len(result), 3):
        entry = {
            'rank': int(result[i]),
            'name': result[i+1],
            'ranking_points': int(result[i+2])
        }
        leaderboard.append(entry)
    return leaderboard


async def get_rank(entrant_name):
    r = await session.get('https://itl2022.groovestats.com/leaderboard')
    await r.html.arender(sleep=1)
    leaderboard = r.html.text.split('\n')[9:-5]

    try:
        ind = leaderboard.index(entrant_name)-1
        return leaderboard[ind]
    except ValueError:
        return "Unknown"

async def get_rank(entrant_name, leaderboard):
    ind = None
    for i, entry in enumerate(leaderboard):
        if entry['name'] == entrant_name:
            ind = i
    
    if ind != None:
        return ind+1
    else:
        return "Unknown"

async def get_ladder(entrant, leaderboard, size=6):
    # yikes, this function turned out to be way harder than I thought it would be
    rivals = []
    for i in range(1, 4):
        if entrant[f'rival{i}']:
            rivals.append(entrant[f'rival{i}'])
    rivals.append(entrant['name'])
    
    # insert a placeholder entrant so that the python indexing matches the ranks
    leaderboard = [{'name': 'placeholder', 'rank': 0, 'ranking_points': 573573573}] + leaderboard

    lookahead = size - len(rivals) - 1
    ladder = []

    # find the (size - #rivals - 1) closest and ahead of the player
    # we look back at most (size-1) ranks since in the worst case we have
    # all the rivals ahead of player. 
    subboard = leaderboard[max(1, entrant['rank']-(size-1)):entrant['rank']]
    subboard.reverse()
    for entry in subboard:
        if entry['name'] not in rivals:
            entry['is_rival'] = False
            entry['is_entrant'] = False
            entry['type'] = 'neutral'
            ladder.append(entry)
        if len(ladder) == lookahead:
            break

    # add the rivals and yourself
    for entry in leaderboard:
        if entry['name'] == entrant['name']:
            entry['is_rival'] = False
            entry['is_entrant'] = True
            entry['type'] = 'self'
            ladder.append(entry)
        elif entry['name'] in rivals:
            entry['is_rival'] = True
            entry['is_entrant'] = False
            entry['type'] = 'rival'
            ladder.append(entry)

    # fill up the ladder, in the rare case that the last ranked player is querying
    # we just return a shorter ladder
    subboard = leaderboard[entrant['rank']+1:min(len(leaderboard), entrant['rank']+5)]
    for entry in subboard:
        if entry['name'] not in rivals:
            entry['is_rival'] = False
            entry['is_entrant'] = False
            entry['type'] = 'neutral'
            ladder.append(entry)
        if len(ladder) == size:
            break

    ladder.sort(key=lambda x: int(x['rank']))
    for entry in ladder:
        entry['difference'] = entrant['ranking_points'] - entry['ranking_points']

    return ladder


async def get_entrant(entrant_id):
    r = await session.get(f'https://itl2022.groovestats.com/entrant/{entrant_id}')
    await r.html.arender(wait=1, sleep=1)
    result = r.html.text.split('\n')[4:29]

    entrant = {'id': entrant_id}
    entrant['name'] = result[0]
    entrant['ranking_points'] = int(result[3])
    entrant['total_points'] = int(result[5])
    entrant['song_points'] = int(result[7])
    entrant['bonus_points'] = int(result[9])
    entrant['passes'] = int(result[12])
    entrant['full_combos'] = int(result[14])
    entrant['full_excellent_combos'] = int(result[16])
    entrant['quad_stars'] = int(result[17])
    entrant['quint_stars'] = int(result[18])
    entrant['rival1'] = None
    entrant['rival2'] = None
    entrant['rival3'] = None
    for i in range(3):
        if result[21+i] == 'Scores Filters':
            for j in range(i+1):
                entrant[f'rival{j+1}'] = result[20+j]

    leaderboard = await get_leaderboard()
    entrant['rank'] = await get_rank(entrant['name'], leaderboard)
    entrant['ladder'] = await get_ladder(entrant, leaderboard, 6)
    # entrant['leaderboard'] = leaderboard

    return entrant