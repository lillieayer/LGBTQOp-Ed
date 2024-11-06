import pandas as pd

def extract_links_from_file(filepath:str) ->list[str]:
    with open(filepath, 'r') as file:
        # cleans out \n and then empty space in list of links
        file_links = [line.strip() for line in file.readlines()]
        file_links = [link for link in file_links if link != '']
    return file_links