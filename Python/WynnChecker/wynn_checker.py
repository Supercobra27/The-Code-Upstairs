import requests
import json
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
import pyarrow.parquet as pq
import pyarrow as pa

load_dotenv()
role_id = os.getenv('ROLE_ID')
discord_hook = os.getenv('DISCORD_HOOK')
embed_color = os.getenv('COLOR')

players_data = {
    'Supercobra28': '84857cf9-d301-4131-a06d-aa3df2488e22',
    'Ssnurch': '6ac2a293-000c-4103-bdf2-4b033c0abd56',
    'Mysty_M': '1b2bfa02-f939-4415-8e5c-5e47466eb87c',
    'AJTA': 'e110a30f-fc47-4f10-88dc-edb95f795fdb',
    'Hal_Leopern': '75cf6bd3-3b45-45db-a165-d1e459b3f6a6',
    'erdbro': '26f7bda7-5e4a-477a-9901-2a5f19f1f94b',
    'AltyMan':'e5d161d7-c1c8-4c3b-9f20-a72c62d2a339'
}

online_map = {
    True : "Online",
    False : "Offline"
}

data = {
    'Player' : [],
    'Combat Level': [],
    'Deaths': [],
    'Total Level': [],
    'Playtime': [],
    'URL': [],
    'Online': [],
}

prof_str = []

for player, class_id in players_data.items():
    api_url_char = f"https://beta-api.wynncraft.com/v3/player/{player}/characters/{class_id}"
    api_url_uuid = f"https://beta-api.wynncraft.com/v3/player/{player}"
    url_char = f"https://wynncraft.com/stats/player/{player}?class={class_id}"
    character_response = requests.get(api_url_char).json()
    online_response = requests.get(api_url_uuid).json()
    professions_response = character_response.get('professions')
    data['Player'].append(player)
    data['Combat Level'].append(character_response.get('level'))
    data['Deaths'].append(character_response.get('deaths'))
    data['Total Level'].append(character_response.get('totalLevel'))
    data['Playtime'].append(character_response.get('playtime'))
    data['Online'].append(online_map[online_response.get('online')])
    data['URL'].append(url_char)
    for prof in professions_response:
        if prof.title() not in data:
            data[prof.title()] = []
        data[prof.title()].append(professions_response.get(prof).get('level'))

df = pd.DataFrame(data)
df = df.sort_values(by='Combat Level', ascending=False)

total_deaths = df['Deaths'].sum()
current_cringe = df.loc[df['Combat Level'].idxmax()]
for col in df.iloc[:, 4:].columns:
    if pd.api.types.is_integer_dtype(df[col]):
        curr_max = df.loc[df[col].idxmax()]
        prof_str.append(f"{curr_max['Player']} ({str(curr_max[col])}) - {col}")

embed = {
    "title": "Most Cringe Player",
    "description": f"Total Deaths: {total_deaths}\nTotal Online: {(df['Online'] == 'Online').sum()}/{len(df['Online'])}",
    "color": embed_color,
    "fields": [
        {
            "name": "Player",
            "value": current_cringe['Player'],
            "inline": True
        },
        {
            "name": "Level",
            "value": str(current_cringe['Combat Level']),
            "inline": True
        },
        {
            "name": "Competition",
            "value": '\n'.join(f"[{row['Player']}]({row['URL']}) ({row['Combat Level']}) [{row['Total Level']}] - {row['Online']}" for _, row in df.iterrows()),
            "inline": False
        },
        {
            "name": "Professions",
            "value": '\n'.join(prof_str),
            "inline": False
        }
    ]
}

cringe_message = {
    "embeds":[embed]
}
requests.post(discord_hook, json=cringe_message)

#df.to_csv('output.csv',index=False)