import pandas as pd
import json
import os



if __name__ == "__main__":
    dir =  './output/control/'
    # make a df for the platform

    data_df = pd.read_json('./output/control/fb_control_engagements.json')
      
    data_df.to_csv(dir + 'fb_control_engagements.csv', index=False)


