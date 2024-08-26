from discord import Intents
from discord import app_commands
from dotenv import load_dotenv
from discord.ui import Button, View
import os
from wynn_functions import *
import asyncio

load_dotenv()
role_id = os.getenv('ROLE_ID')
discord_hook = os.getenv('DISCORD_HOOK')
embed_color = os.getenv('COLOR')
discord_token = os.getenv('DISCORD_TOKEN')
guild_id=os.getenv('GUILD_ID')

players_data = {
    'Supercobra28': '84857cf9-d301-4131-a06d-aa3df2488e22',
    'Ssnurch': '6ac2a293-000c-4103-bdf2-4b033c0abd56',
    'Mysty_M': '1b2bfa02-f939-4415-8e5c-5e47466eb87c',
    'AJTA': 'e110a30f-fc47-4f10-88dc-edb95f795fdb',
    'Hal_Leopern': '75cf6bd3-3b45-45db-a165-d1e459b3f6a6',
    'erdbro': '26f7bda7-5e4a-477a-9901-2a5f19f1f94b',
    'AltyMan':'e5d161d7-c1c8-4c3b-9f20-a72c62d2a339'
}

class ClassView(View):
    def __init__(self, buttons, ign):
        super().__init__()
        self.ign = ign
        for custom_id,label in buttons:
            button = Button(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
            button.callback = self.button_callback
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print(interaction.data.get('custom_id'))
        return True
    
    async def button_callback(self, interaction: discord.Interaction):
        for item in self.children:
            item.disabled = True
        
        global players_data
        players_data[self.ign] = interaction.data.get('custom_id')
        await interaction.response.send_message(f'Successfully updated the data with {self.ign} with class {players_data[self.ign]}')


async def reload_data():
    while True:
        print("Reloading Data...")
        global current_load
        current_load = collect_player_data(players_data)
        print("Reload Complete")
        await asyncio.sleep(60)

intents = Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
current_load = pd.DataFrame()

@client.event
async def on_ready():
    try:
        client.loop.create_task(reload_data())
        await tree.sync(guild=discord.Object(id=guild_id))
        print(f'Logged in as {client.user}')
    except Exception as e:
        print(e)

@tree.command(
    name="wynnload",
    description="Reloads all data",
    guild=discord.Object(id=guild_id)
)
async def wynnload(interaction: discord.Interaction):  
    await interaction.response.send_message('Reloading...')        
    df = collect_player_data(players_data)
    await interaction.response.send_message('Loaded.')
    global current_load
    current_load = df

@tree.command(
    name="wynntop",
    description="Loads the most cringe person in Wynncraft",
    guild=discord.Object(id=guild_id)
)

async def wynntop(interaction: discord.Interaction):
    df = current_load[0]
    try:
        total_deaths = df['Deaths'].sum()
        current_cringe = df.loc[df['Combat Level'].idxmax()]        
        # Define embed details
        embed_title = "Most Cringe Player"
        embed_description = (
        f"Total Deaths: {total_deaths}\n"
        f"Total Online: {(df['Online'] == 'Online').sum()}/{len(df['Online'])}"
        )
        embed_color = discord.Color.red()

    # Create the embed object
        temp_embed = discord.Embed(
        title=embed_title,
        description=embed_description,
        color=embed_color
        )

# Add fields to the embed
        fields = [
        ("Player", current_cringe['Player'], True),
        ("Level", str(current_cringe['Combat Level']), True),
        ("Competition", '\n'.join(
        f"[{row['Player']}]({row['URL']}) ({row['Combat Level']}) [{row['Total Level']}]"
        for _, row in df.iterrows()
            ), False)
        ]
        for name, value, inline in fields:
            temp_embed.add_field(name=name, value=value, inline=inline)
        await interaction.response.send_message(embed=temp_embed)
    except Exception as e:
        await interaction.response.send_message(embed=create_error(e))

@tree.command(
    name="wynnonline",
    description="Lists all online players",
    guild=discord.Object(id=guild_id)
)

async def wynnonline(interaction: discord.Interaction):
    try:
        df = current_load[0]
        online_embed = discord.Embed(
            title="Players Online",
            color=discord.Color.green(),
            description=f"Total Online: {(df['Online'] == 'Online').sum()}/{len(df['Online'])}"
        )
        online_embed.add_field(name="Player List",value='\n'.join(f"{row['Player']} - {row['Online']}" for _, row in df.iterrows()), inline=False)
        await interaction.response.send_message(embed=online_embed)
    except Exception as e:
        await interaction.response.send_message(embed=create_error(e))

@tree.command(
    name="wynnprofs",
    description="Lists profession leaderboard",
    guild=discord.Object(id=guild_id)
)

async def wynnprofs(interaction: discord.Interaction):
    try:
        prof_str = current_load[1]
        online_embed = discord.Embed(
            title="Players Professions",
            color=discord.Color.green(),
            description=f"Player Professions"
        )
        online_embed.add_field(name="Player Professions",value='\n'.join(prof_str), inline=False)
        await interaction.response.send_message(embed=online_embed)
    except Exception as e:
        await interaction.response.send_message(embed=create_error(e))

@tree.command(
    name="wynn",
    description="Yes",
    guild=discord.Object(id=guild_id)
)
async def wynn(interaction: discord.Interaction):
    await interaction.response.send_message("play.wynncraft.com")
    
@tree.command(
    name="wynnadd",
    description="Adds a player to the loading parameters",
    guild=discord.Object(id=guild_id)
)
async def wynnadd(interaction: discord.Interaction, ign: str):
    global current_load
    char_dict = current_load[2]
    buttons = []
    for char in char_dict[ign]:
        buttons.append(tuple(char.values()))
    view = ClassView(buttons,ign)
    await interaction.response.send_message(f'Select a character...', view=view)

@tree.command(
    name="wynndel",
    description="Adds a player to the loading parameters",
    guild=discord.Object(id=guild_id)
)
async def wynndel(interaction: discord.Interaction, ign: str):
    global players_data
    await interaction.response.send_message(f'Succesfully deleted {ign} with class ID {players_data[ign]}')
    del players_data[ign]


client.run(discord_token)