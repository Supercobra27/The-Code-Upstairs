import discord
import pandas as pd
import requests
from wynn_maps import *

def create_error(e):
    error_embed = discord.Embed(
        title="An Error Occurred",
        description=f"```{str(e)}```",
        color=discord.Color.red()
    )
    return error_embed

def collect_player_data(players_data):
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
    char_dict = {}

    for player, class_id in players_data.items():
            api_url_char = f"https://beta-api.wynncraft.com/v3/player/{player}/characters/{class_id}"
            api_url_uuid = f"https://beta-api.wynncraft.com/v3/player/{player}"
            api_url_characters = f"https://beta-api.wynncraft.com/v3/player/{player}/characters"
            url_char = f"https://wynncraft.com/stats/player/{player}?class={class_id}"
            character_response = requests.get(api_url_char).json()
            online_response = requests.get(api_url_uuid).json()
            char_response = requests.get(api_url_characters).json()
            char_dict[player] = []
            for char in list(char_response.keys()):
                char_type = char_response.get(char).get('type')
                char_level = char_response.get(char).get('level')
                char_dict[player].append({
                    "id":char,
                    "class":f"{char_level} - {char_type}"
                })
            data['Player'].append(player)
            data['Combat Level'].append(character_response.get('level'))
            data['Deaths'].append(character_response.get('deaths'))
            data['Total Level'].append(character_response.get('totalLevel'))
            data['Playtime'].append(character_response.get('playtime'))
            data['Online'].append(online_map[online_response.get('online')])
            data['URL'].append(url_char)

            professions_response = character_response.get('professions')
            for prof in professions_response:
                if prof.title() not in data:
                    data[prof.title()] = []
                data[prof.title()].append(professions_response.get(prof).get('level'))

            df = pd.DataFrame(data)
            df = df.sort_values(by='Combat Level', ascending=False)
            df.to_csv('player_data.csv', index=False)
            for col in df.iloc[:, 4:].columns:
                if pd.api.types.is_integer_dtype(df[col]):
                    curr_max = df.loc[df[col].idxmax()]
                    prof_str.append(f"{curr_max['Player']} ({str(curr_max[col])}) - {col}")
    return df,prof_str[:12],char_dict