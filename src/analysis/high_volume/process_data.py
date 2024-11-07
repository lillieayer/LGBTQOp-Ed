import pandas as pd
import json



if __name__ == "__main__":
    filename = 'lakewood_shooter_engagements.json'
    dir =  './output/high_volume/fb/'
    data_df = pd.read_json(dir+filename)
    data_df.to_csv(dir+'lakewood_engagements.csv', index=False)
    print(data_df.head)


