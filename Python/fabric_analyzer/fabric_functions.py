import subprocess
import os
import pandas as pd

def check_directory(gfilepath:str,obsidian_folder:str):
    obsidian_folder = f'{gfilepath}\\{obsidian_folder}'
    if not os.path.exists(obsidian_folder):
        os.makedirs(obsidian_folder)
        print(f"Directory {obsidian_folder} created.")
    else:
        print(f"Directory {obsidian_folder} already exists.")

def run_shell_command(command: str):
    try:
        # Run the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Decode the output from binary to string
        output = result.stdout.decode('utf-8')
        
        # Remove \r and replace \n with Markdown line breaks
        cleaned_output = output.replace('\r', '').replace('\n', '  \n')
        
        return cleaned_output
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode('utf-8')
        print(f"An error occurred while executing the command: {e}")
        print(f"Error output: {error_output}")
        return None
    
def create_yt_note(filepath: str, pdrow: pd.Series):
    cmd = f'yt --transcript {pdrow["link"]} | fabric --pattern {pdrow["pattern"]}'
    check_directory(filepath, pdrow["folder"])
    obsidian_note = open(f'{filepath}\\{pdrow["folder"]}\\{pdrow["title"]}.md', "w")
    result = run_shell_command(cmd)
    print('---\ntags:\n- Fabric_Generated\n---', file=obsidian_note)
    print(f'# AI Extraction - {pdrow["pattern"]}', file=obsidian_note)
    print(result, file=obsidian_note)
