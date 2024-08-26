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
    'Status': []
}

prof_str = []

for player, class_id in players_data.items():
    api_url_uuid = f"https://beta-api.wynncraft.com/v3/player/{player}"
    online_response = requests.get(api_url_uuid).json()
    data['Player'].append(player)
    data['Status'].append(online_map[online_response.get('online')])

df = pd.DataFrame(data)
print(df)