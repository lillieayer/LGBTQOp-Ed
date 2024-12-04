import pandas as pd
import os

'''
Specialized for specifying narrative data and combining into one dataframe per social platform'''

def combine_dir_files_as_df(dir):
    all_files_df = []
    for file in os.listdir(dir):
       
        file_df = pd.read_json(dir+file)
        filename = file.split('.')[0]
        # specify narrative from file its taken from
        file_df['NARRATIVE'] = filename
        all_files_df.append(file_df)
    
    all_files_df = pd.concat(all_files_df, ignore_index=True)
    return all_files_df

 


