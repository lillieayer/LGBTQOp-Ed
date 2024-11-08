import pandas as pd
import json
import os



if __name__ == "__main__":
    dir =  './output/high_volume/twitter/'
    # make a df for the platform
    narrative_df = []
    for file in os.listdir(dir):
       
        data_df = pd.read_json(dir+file)
        filename = file.split('.')[0]
        data_df['NARRATIVE'] = filename
        narrative_df.append(data_df)
    
    platform_df = pd.concat(narrative_df, ignore_index=True)
    platform_df.to_csv(dir+'engagements.csv', index=False)


