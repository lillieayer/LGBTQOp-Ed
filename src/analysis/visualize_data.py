import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from process_data import *

narrative_labels = {
    'tampons': "Tim Walz mandated tampons in boys' bathrooms",
    'target': "Children's tuck-friendly bathing suits at Target",
    'lakewood':"Lakewood Church shooter identified as transgender"

}

twitter_df = combine_dir_files_as_df('./output/twitter')
fb_df = combine_dir_files_as_df('./output/fb')
fbcontrol_df = pd.read_json('./output/control/fb_control_engagements.json')
tcontrol_df = pd.read_csv('./output/control/twitter_control_engagements.json')

def clean_control_data():
  fbcontrol_df.loc[fbcontrol_df['LINK'] == "https://www.facebook.com/ToddStarnesFNC/posts/pfbid036d1sYedZqHYMA4rFdjy9tU49KMbL5xTtk7ta5e2thfSqyTQ8gPxFJwYa2Gh9MLujl", 'REACTIONS'] = 97
  fbcontrol_df.loc[fbcontrol_df['LINK'] == "https://www.facebook.com/ToddStarnesFNC/posts/pfbid036d1sYedZqHYMA4rFdjy9tU49KMbL5xTtk7ta5e2thfSqyTQ8gPxFJwYa2Gh9MLujl", 'COMMENTS'] = 30
  fbcontrol_df.loc[fbcontrol_df['LINK'] == "https://www.facebook.com/ToddStarnesFNC/posts/pfbid036d1sYedZqHYMA4rFdjy9tU49KMbL5xTtk7ta5e2thfSqyTQ8gPxFJwYa2Gh9MLujl", 'SHARES'] = 3
  fbcontrol_df['NARRATIVE'] = "Control Group"
  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/SaraGonzalesTX/status/1856860763173814286", 'RETWEETS'] = 30
  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/SaraGonzalesTX/status/1856860763173814286", 'LIKES'] = 353

  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/ClayTravis/status/1856857613243179221", 'RETWEETS'] = 7
  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/ClayTravis/status/1856857613243179221", 'LIKES'] = 119


  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/scarlett4kids/status/1858027540830412826", 'RETWEETS'] = 4
  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/scarlett4kids/status/1858027540830412826", 'LIKES'] = 15


  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/scarlett4kids/status/1857101714995753406", 'RETWEETS'] = 6
  tcontrol_df.loc[tcontrol_df['LINK'] == "https://x.com/scarlett4kids/status/1857101714995753406", 'LIKES'] = 47
  tcontrol_df['NARRATIVE'] = "Control Group"

def clean_fb_data():
  # clean fb dataset entries
  fb_df.drop([1,3], inplace=True)
  fb_df.drop([5], inplace=True)
  fb_df.drop([7], inplace=True)
  new_row1 = pd.DataFrame({'LINK': ["https://www.facebook.com/TheFederalistPapers/posts/pfbid02BXpsVYtSTsWJWCXCC8qvZLTygXbGxrLcGjALKhKdf4LoGyZVCYX4quXZo31NWJU3l"], 'REACTIONS': [4900], "COMMENTS":[1300] , "SHARES":[2600], 'CONTENT':[''], 'AUTHOR':[''], 'NARRATIVE':["Children's tuck-friendly bathing suits at Target"] })
  new_row = pd.DataFrame({'LINK': ["https://www.facebook.com/ToddStarnesFNC/posts/pfbid0ZZhDixJQuaFoB8VLNYXuJrgd1oKnxuBvYLmMR5YeoD4CdxYxpu5cedAvTcwgWXFAl"], 'AUTHOR': ["Todd Starnes"], 'CONTENT': ["Tim Walz signed a law putting tampons in boys' bathrooms in taxpayer-funded schools. "], 'REACTIONS':[445.0], 'COMMENTS':[262.0], 'SHARES':[287.0], 'NARRATIVE':"Tim Walz mandated tampons in boys' bathrooms"})
  fb_df = pd.concat([fb_df, new_row], ignore_index=True)
  fb_df = pd.concat([fb_df,new_row1], ignore_index=True)
  fb_df.dropna(inplace=True)

def add_narrative_desc():
  fb_df.loc[fb_df['NARRATIVE'] == "walz_tampons_engagements", 'NARRATIVE'] = "Tim Walz mandated tampons in boys' bathrooms"
  fb_df.loc[fb_df['NARRATIVE'] == "lakewood_shooter_engagements", 'NARRATIVE'] = "Lakewood Church shooter identified as transgender"
  fb_df.loc[fb_df['NARRATIVE'] == "target_suits_engagements", 'NARRATIVE'] = "Children's tuck-friendly bathing suits at Target"
  twitter_df.loc[twitter_df['NARRATIVE'] == "target_suits_engagements", 'NARRATIVE'] = "Children's tuck-friendly bathing suits at Target"
  twitter_df.loc[twitter_df['NARRATIVE'] == "lakewood_shooter_engagements", 'NARRATIVE'] = "Lakewood Church shooter identified as transgender"
  twitter_df.loc[twitter_df['NARRATIVE'] == "walz_tampons_engagements", 'NARRATIVE'] = "Tim Walz mandated tampons in boys' bathrooms"


all_data = pd.concat([fb_df, fbcontrol_df])
new_order = [0,2,3,1]
narrative_data = all_data.groupby('NARRATIVE')[['REACTIONS', 'COMMENTS', 'SHARES']].mean()
narrative_data = narrative_data.iloc[new_order]
narrative_data.head()

plt.figure(figsize=(15, 6))
x = np.arange(4)
width = 0.25
plt.bar(x - width, narrative_data['REACTIONS'], width, label=f'Reactions', color='r', edgecolor='grey')
plt.bar(x, narrative_data['COMMENTS'], width, label=f'Comments', color='g', edgecolor='grey')
plt.bar(x + width, narrative_data['SHARES'], width, label=f'Shares', color='b', edgecolor='grey')
plt.xticks(x, narrative_data.index, rotation=45)
plt.xlabel('Narratives')
plt.ylabel('Average Number of Engagements Per Post')
plt.title('Average Engagements Across Several Narratives on Facebook')
plt.legend()
plt.savefig('drive/MyDrive/DisinfoGraphs/fb_high_volume_chart.jpeg', format='jpeg',bbox_inches='tight', pad_inches=0.2)
plt.show()

all_data = pd.concat([twitter_df, tcontrol_df])
new_order = [0,2,3,1]
narrative_data = all_data.groupby('NARRATIVE')[['LIKES', 'RETWEETS']].mean()
narrative_data = narrative_data.iloc[new_order]
narrative_data.head()

plt.figure(figsize=(15, 6))
x = np.arange(4)
width = 0.25
plt.bar(x - width, narrative_data['LIKES'], width, label=f'Likes', color='r', edgecolor='grey')
#plt.bar(x, narrative_data['COMMENTS'], width, label=f'Comments', color='g', edgecolor='grey')
plt.bar(x, narrative_data['RETWEETS'], width, label=f'Retweets', color='b', edgecolor='grey')
plt.xticks(x, narrative_data.index, rotation=45)
plt.xlabel('Narratives')
plt.ylabel('Average Number of Engagements Per Post')
plt.title('Average Engagements Across Several Narratives on Twitter')
plt.legend()
plt.savefig('drive/MyDrive/DisinfoGraphs/twitter_high_volume_chart.jpeg', format='jpeg',bbox_inches='tight', pad_inches=0.2)
plt.show()

all_data1 = pd.concat([twitter_df, tcontrol_df])
all_data1 = all_data1.rename(columns={'RETWEETS': 'SHARES'})
all_data2 = pd.concat([fb_df, fbcontrol_df])
all_data2 = all_data2.rename(columns={"REACTIONS" : "LIKES"})
new_order = [0,2,3,1]
all_data = pd.concat([all_data1, all_data2])
narrative_data = all_data.groupby('NARRATIVE')[['LIKES', 'SHARES']].mean()
narrative_data = narrative_data.iloc[new_order]
narrative_data.head()

plt.figure(figsize=(15, 6))
x = np.arange(4)
width = 0.25
plt.bar(x - width, narrative_data['LIKES'], width, label='Likes', color='r', edgecolor='grey')
#plt.bar(x, narrative_data['QUOTES'], width, label=f'Quotes', color='g', edgecolor='grey')
plt.bar(x, narrative_data['SHARES'], width, label='Shares', color='b', edgecolor='grey')
plt.xticks(x, narrative_data.index, rotation=45)
plt.xlabel('Narratives')
plt.ylabel('Average Number of Engagements Per Post')
plt.title('Average Engagements Across Several Narratives on Twitter and FaceBook')
plt.legend()
plt.savefig('drive/MyDrive/DisinfoGraphs/all_high_volume_chart.jpeg', format='jpeg',bbox_inches='tight', pad_inches=0.2)
plt.show()


fb_dates = {
'https://www.facebook.com/RepMTGreene/posts/pfbid02oSMjyoxunCaNLVGX2eSnpGZuD9jzksEAyZnnhrJRGVVN9XDQRWcc6iD7nDV3ki6el':'2024-02-12 02:05:00 PM',
'https://www.facebook.com/drmichaelsavage/posts/pfbid021uf7mJURoP3Ano9wDU1Fy8d2bHY1qFR7UViXZv5cQ9c5ueQihp8Vf8CbZd2QHBoWl':'2024-02-13 12:11:00 PM',
'https://www.facebook.com/secureamericanow/posts/pfbid02KVnTKbn1dRUHqEwNQSPTjGoUQj8YrTQXU99MywNrTnZBvBRRW9YumDKHAixJCAPWl':'2024-02-12 10:32:00 PM',
'https://www.facebook.com/mediaresearchcenter/posts/pfbid08tAhvPEbqgPrxvXZ126cUomTGXP26azJEvpb4tD54DMV84V4T3PriEtZvYfNjkjBl':'2024-02-13 12:28:00 PM',
'https://www.facebook.com/pamelageller/posts/pfbid034FjA3nJF3PmJPdcCA3hFD4scW17n62honhRbZBU1WDkVHMvVVJopTYWQcpNqhyXml':'2024-02-12 02:13:00 PM',
'https://www.facebook.com/TheDallasExpress/posts/pfbid02mzUnmLeniPswJGgve8pQ52TbvM5voQm1Ez3eSqvTGeYZxXb5G2tZSg9TqXrSw7q6l':'2024-02-12 03:36:00 PM',
'https://www.facebook.com/Sarah.Fields1836/posts/pfbid02HhVbxsgT7N4xouhte8FyVFgfniSJR33GVLSKw5aqZmXoMAkmmK1owUbMqmpWUhvnl':'2024-02-12 02:36:00 PM',
'https://www.facebook.com/OutkickTheCoverage/posts/pfbid02cbxZY5BbhoVTA7HTR1wuL8zKMPxdh38tc9g22aoG1g5BMpMYZiW9L3kGX1EgL79ql':'2024-05-10 06:32:00 PM',
'https://www.facebook.com/ChristianPost.Intl/posts/pfbid038M3LtBLWPf4srDr8mALJkVHzLCbbBKVb52CUDRJcdh65aZ8zitKXVob8v5iemF6Zl':'2023-05-30 02:02:00 PM',
'https://www.facebook.com/MattWalshBlog/posts/pfbid02KbFATjWk3gotbYghCTgrPtJ1qmt3u8wP3bFtffGmERsfmC37yF3PkQNqr8vJtJg1l':'2024-05-11 10:17:00 AM',
'https://www.facebook.com/TheFederalistPapers/posts/pfbid02BXpsVYtSTsWJWCXCC8qvZLTygXbGxrLcGjALKhKdf4LoGyZVCYX4quXZo31NWJU3l':'2023-05-21 02:15:00 PM',
'https://www.facebook.com/lilagracerose/posts/pfbid0V7JY1SbePSWh2yj3MYNijMJNUrSN4Zo8fXVd8hxBS2ApeUtP6K2LD3r2zu7QgkrBl':'2023-05-24 05:32:00 PM',
'https://www.facebook.com/lilagracerose/posts/pfbid0rhPys2dk9GELUx2t9taNgTQAAHe8vjP2ywPtzecgqWNwHrESV5CgbrcRanKobE4Jl':'2024-05-20 01:03:00 PM',
'https://www.facebook.com/ThePostMillennial/posts/pfbid0E5Uj5YYoDD3MseZUMiT6tFm9HpH1bCtdKX7rbyQTJpkUXdwrit1aPMpJuv85ueYBl':'2024-08-07 10:43:00 AM',
'https://www.facebook.com/ToddStarnesFNC/posts/pfbid0ZZhDixJQuaFoB8VLNYXuJrgd1oKnxuBvYLmMR5YeoD4CdxYxpu5cedAvTcwgWXFAl':'2024-08-06 04:05:00 PM',
'https://www.facebook.com/MegynKelly/posts/pfbid02zoDbDgc2ZGt26P28ve77vkgagegVVFkLcRhSGZmgVndWcRrJjES36vHWQBSiBDeil':'2024-08-12 08:00:00 PM',
'https://www.facebook.com/mediaresearchcenter/posts/pfbid037pF6w2W4bH5DhcNTcANSwprWg3WvfNx7S7oinYV9Xf57THro3JcsrLqVHERbcCTsl':'2024-08-08 01:30:00 PM',
'https://www.facebook.com/abbyjohnsonprolife/posts/pfbid02HvV5JApRWdyH48PFvspcBfvgMiuFefnfj4ztbsa16xEbP3Xke5C4RbS3sZbuFvxbl':'2024-08-06 01:44:00 PM',
'https://www.facebook.com/NYPost/posts/pfbid0hrseMufRJXehirsEbJkKQxETficEoRsC8EdnrYmJwK47hdQvJJnMF4q27RAKn7yrl':'2024-08-08 11:06:00 PM',
'https://www.facebook.com/KevinSteeleTV/posts/pfbid0Q9eK8rGNu7p4RRvWqGczvTmoGmWTeug6sZEZhUZ4ixitrtMAwRFCVxeCpy1BD2Gql':'2024-08-06 08:22:00 PM',
'https://www.facebook.com/permalink.php?story_fbid=pfbid0VK6dML7JeYPH527GPPVcPE7Lvcav6oQeMMKhzmbJjhKi9xUrQ77v57bDqHvLWd23l&id=100044196440904':'2024-08-06 11:00:00 AM'
}

fb_df['DATE'] = np.nan
for key in fb_dates:
  fb_df.loc[fb_df['LINK'] == key, 'DATE'] = fb_dates[key]

fb_df['DATE'] = pd.to_datetime(fb_df['DATE'])
from datetime import datetime
def convert_to_date(string):
  string = datetime.strptime(string, "%I:%M %p · %b %d, %Y")
  return string
twitter_df['DATE'] = twitter_df['DATE'].apply(lambda x: convert_to_date(x))

tampon_start_fb = fb_df[fb_df['NARRATIVE'] == "Tim Walz mandated tampons in boys' bathrooms"]["DATE"]
tampon_start_twitter = twitter_df[twitter_df['NARRATIVE'] == "Tim Walz mandated tampons in boys' bathrooms"]["DATE"]
print(tampon_start_fb)
print(tampon_start_twitter)
tampon_start_time = pd.to_datetime('2024-08-06 9:57AM')

lakewood_start_fb = fb_df[fb_df['NARRATIVE'] == "Lakewood Church shooter identified as transgender"]["DATE"]
lakewood_start_twitter = twitter_df[twitter_df['NARRATIVE'] == "Lakewood Church shooter identified as transgender"]["DATE"]
print(lakewood_start_fb.min())
print(lakewood_start_twitter.min())
lakewood_start_time = pd.to_datetime('2024-02-12 10:44PM')


# combine all dataframes

all_times = pd.concat([twitter_df, fb_df], axis=0)
all_times = all_times[['NARRATIVE', 'DATE']]
all_times['MONTH'] = all_times['DATE'].dt.strftime('%B')
all_times['MONTH'] = pd.Categorical(all_times['MONTH'], categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
all_times['YEAR'] = all_times['DATE'].dt.strftime('%Y')
all_times['YEAR'] = pd.Categorical(all_times['YEAR'], categories=['2023', '2024'])
start_times = all_times.groupby('NARRATIVE')['DATE'].min()
target_start_time = start_times.iloc[0]
lakewood_start_time = start_times.iloc[1]
tampons_start_time = start_times.iloc[2]

lakewood_df = all_times[all_times['NARRATIVE'] == "Lakewood Church shooter identified as transgender"]
tampons_df = all_times[all_times['NARRATIVE'] == "Tim Walz mandated tampons in boys' bathrooms"]
target_df = all_times[all_times['NARRATIVE'] == "Children's tuck-friendly bathing suits at Target"]

lakewood_df['DIFF'] = abs(lakewood_df.loc[:,'DATE'] - lakewood_start_time)
tampons_df['DIFF'] = abs(tampons_df.loc[:,'DATE'] - tampons_start_time)
target_df['DIFF'] = abs(target_df.loc[:,'DATE'] - target_start_time)
lakewood_df['total_hours'] = lakewood_df['DIFF'].dt.total_seconds()/ 3600
lakewood_df['total_days'] = lakewood_df.loc[:,'total_hours'] // 24
tampons_df['total_hours'] = tampons_df.loc[:,'DIFF'].dt.total_seconds()/3600
tampons_df['total_days'] = tampons_df.loc[:,'total_hours'] // 24
target_df['total_hours'] = target_df.loc[:,'DIFF'].dt.total_seconds()/3600
target_df['total_days'] = target_df.loc[:,'total_hours'] // 24

# get series to get the cumulative of posts as days pass
sum_freq_target = target_df['total_days'].value_counts().sort_index().cumsum()
sum_freq_tampons = tampons_df['total_days'].value_counts().sort_index().cumsum()
sum_freq_lakewood = lakewood_df['total_days'].value_counts().sort_index().cumsum()

print(target_df['total_days'].value_counts())
# based on value counts best to capture target data within 2 weeks --> bulk from 5-11 day range

print(tampons_df['total_days'].value_counts())
# based on value counts best to capture tampon data within 3 days, bulk from 0-5 day range

print(lakewood_df['total_days'].value_counts()) # builk within 1 day

# get it by hours
sum_freq_target_hr = target_df['total_hours'].value_counts().sort_index().cumsum()
sum_freq_tampons_hr = tampons_df['total_hours'].value_counts().sort_index().cumsum()
sum_freq_lakewood_hr = lakewood_df['total_hours'].value_counts().sort_index().cumsum()

# plot all narratives on line plot over time
plt.figure(figsize=(13, 5))
sum_freq_target.plot(label="Children's tuck-friendly bathing suits at Target", color='b')
sum_freq_lakewood.plot(label="Lakewood Church shooter identified as transgender", color='g')
sum_freq_tampons.plot(label="Tim Walz mandated tampons in boys' bathrooms", color='r')
plt.legend()

plt.ylabel("Cumulative sum of posts dispersed")
plt.xlabel("Time passed since inital posting (in days)")
plt.title("Post Dispersion of Disinformant Narratives")
plt.xticks(np.arange(0,360,25))
plt.yticks(np.arange(0,20,1))
#plt.savefig('drive/MyDrive/DisinfoGraphs/target_rapid_chart.jpeg', format='jpeg')
# Show the plot
plt.show()

# plot all narratives on line plot over 2 weeks span
plt.figure(figsize=(10, 5))
day_thresh = 7
target2wks = sum_freq_target[sum_freq_target.index <= day_thresh]
tampons2wks = sum_freq_tampons[sum_freq_tampons.index <= day_thresh]
lake2wks = sum_freq_lakewood[sum_freq_lakewood.index <= day_thresh]

target2wks.plot(label="Children's tuck-friendly bathing suits at Target", color='b', marker='o')
lake2wks.plot(label="Lakewood Church shooter identified as transgender", color='g', marker='s')
tampons2wks.plot(label="Tim Walz mandated tampons in boys' bathrooms", color='r', marker='^')
plt.legend()

plt.ylabel("Number of posts dispersed")
plt.xlabel("Time passed since inital posting (in days)")
plt.title("Post Dispersion of Disinformant Narratives Within 1 Week")
plt.xticks(np.arange(0,8,1))
plt.yticks(np.arange(0,20,1))
plt.savefig('drive/MyDrive/DisinfoGraphs/all_line_1weeks.jpeg', format='jpeg')
# Show the plot
plt.show()

# plot all narratives on line plot over 2 days in hours
plt.figure(figsize=(12, 6))
hr_thresh = 3*24
target36hr = sum_freq_target_hr[sum_freq_target_hr.index <= hr_thresh]
tampons36hr = sum_freq_tampons_hr[sum_freq_tampons_hr.index <= hr_thresh]
lake36hr = sum_freq_lakewood_hr[sum_freq_lakewood_hr.index <= hr_thresh]

target36hr.plot(label="Children's tuck-friendly bathing suits at Target", color='b', marker='o')
lake36hr.plot(label="Lakewood Church shooter identified as transgender", color='g', marker='s')
tampons36hr.plot(label="Tim Walz mandated tampons in boys' bathrooms", color='r', marker='^')
plt.legend()

plt.ylabel("Number of posts dispersed")
plt.xlabel("Time passed since inital posting (in hours)")
plt.title("Post Dispersion of Disinformant Narratives Within 2 days")
plt.xticks(np.arange(0,hr_thresh+1,5))
plt.yticks(np.arange(0,20,1))
#plt.savefig('drive/MyDrive/DisinfoGraphs/all_line_36hr.jpeg', format='jpeg')
# Show the plot
plt.show()

# get total posts per narrative
total_posts_target = sum_freq_target.iloc[-1]
total_posts_tampons = sum_freq_tampons.iloc[-1]
total_posts_lake = sum_freq_lakewood.iloc[-1]
threshold = 2 # change this to get dif % results
tar = sum_freq_target[sum_freq_target.index <= threshold]
tam = sum_freq_tampons[sum_freq_tampons.index <= threshold]
lak = sum_freq_lakewood[sum_freq_lakewood.index <= threshold]
# basic var names ot switch time threshold
max_lak = lak.iloc[-1]
max_tar= tar.iloc[-1]
max_tam = tam.iloc[-1]
# calculate % of posts posted within 2 days
p_tar= round((max_tar / total_posts_target) * 100,2)
p_lak = round((max_lak / total_posts_lake) * 100,2)
p_tam= round((max_tam / total_posts_tampons) * 100,2)
print(f"{p_tar}% target posts within {threshold} days")
print(f"{p_tam}% tampons posts within {threshold} days")
print(f"{p_lak}% lakewood posts within {threshold} days")

# plot all narratives within the 2 week mark
plt.figure(figsize=(13, 5))
l2week = lakewood_df.loc[lakewood_df['total_days'] < 7]
t2week = target_df.loc[target_df['total_days'] < 14]
ta2week = tampons_df.loc[tampons_df['total_days'] < 7]
#plt.hist(ta2week['total_days'], edgecolor='grey', bins=10, color='r', label="Tim Walz mandated tampons in boys' bathrooms")
#plt.hist(l2week['total_days'], edgecolor='grey',  bins=10, color='g', label="Lakewood Church shooter identified as transgender")
plt.hist(t2week['total_days'], edgecolor='grey', color='b', label="Children's tuck-friendly bathing suits at Target posts from 2023")
#plt.legend()

plt.ylabel("Number of posts dispersed")
plt.xlabel("Time passed since inital posting (in days)")
plt.title("Post Dispersion of Tuck-free Bathing Suit Narrative within 2 weeks")
plt.savefig('drive/MyDrive/DisinfoGraphs/target_rapid_chart.jpeg', format='jpeg')
# Show the plot
plt.show()

# plot all narratives within the 2 week mark
plt.figure(figsize=(10, 5))
l2week = lakewood_df.loc[lakewood_df['total_days'] < 3]
t2week = target_df.loc[target_df['total_days'] < 3]
ta2week = tampons_df.loc[tampons_df['total_days'] < 3]
plt.hist(ta2week['total_days'], edgecolor='grey', color='r', label="Tim Walz mandated tampons in boys' bathrooms")
plt.hist(l2week['total_days'], edgecolor='grey', color='g', label="Lakewood Church shooter identified as transgender")
plt.hist(t2week['total_days'], edgecolor='grey', color='b', label="Children's tuck-friendly bathing suits at Target posts from 2023")
plt.legend()
plt.xticks(np.arange(0,4, 1))
plt.ylabel("Number of posts dispersed")
plt.xlabel("Time passed since inital posting (in days)")
plt.title("Post Dispersion of Disinformant Narratives within 1 week")
#plt.savefig('drive/MyDrive/DisinfoGraphs/target_rapid_chart.jpeg', format='jpeg')
# Show the plot
plt.show()

plt.figure(figsize=(10, 5))
l2week = lakewood_df.loc[lakewood_df['total_days'] < 3]
t2week = target_df.loc[target_df['total_days'] < 3]
ta2week = tampons_df.loc[tampons_df['total_days'] < 3]
plt.hist(ta2week['total_hours'], edgecolor='grey', color='r', label="Tim Walz mandated tampons in boys' bathrooms")
plt.hist(l2week['total_hours'], edgecolor='grey', color='g', label="Lakewood Church shooter identified as transgender")
plt.hist(t2week['total_hours'], edgecolor='grey', color='b', label="Children's tuck-friendly bathing suits at Target posts from 2023")
plt.legend()
plt.ylabel("Number of posts dispersed")
plt.xlabel("Time passed since inital posting (in days)")
plt.title("Post Dispersion of Disinformant Narratives within 1 week")
#plt.savefig('drive/MyDrive/DisinfoGraphs/target_rapid_chart.jpeg', format='jpeg')
# Show the plot
plt.show()

l2week = lakewood_df.loc[lakewood_df['total_days'] < 7]
t2week = target_df.loc[target_df['total_days'] < 7]
ta2week = tampons_df.loc[tampons_df['total_days'] < 7]
all_1week = pd.concat([l2week, t2week, ta2week])
all_1week.head()

plt.figure(figsize=(15,6))
custom_colors = {"Children's tuck-friendly bathing suits at Target": 'blue', "Lakewood Church shooter identified as transgender": 'green',"Tim Walz mandated tampons in boys' bathrooms":'red' }
sns.stripplot(x='total_hours', y='YEAR',data=all_1week,hue='NARRATIVE', jitter=True, size=7, alpha=0.6, palette=custom_colors)
plt.title("Dispersion of Narratives on Twitter and FaceBook within One Week")
plt.xlabel("Time passed from earliest post (in hours)")
plt.ylabel("Year")
plt.xticks(np.arange(0,170, 5))
plt.legend()
plt.savefig('drive/MyDrive/DisinfoGraphs/all_rapid_scatter_chart.jpeg', format='jpeg', bbox_inches='tight', pad_inches=0.2)
plt.show()


lakewood_monthly = lakewood_df['DATE'].dt.strftime("%B %Y")
target_monthly = target_df['DATE'].dt.strftime("%B %Y")
tampons_monthly = tampons_df['DATE'].dt.strftime("%B %Y")
custom_colors = {"Children's tuck-friendly bathing suits at Target": 'blue', "Lakewood Church shooter identified as transgender": 'green',"Tim Walz mandated tampons in boys' bathrooms":'red' }
x = [datetime(2024, month, 1).strftime("%B") for month in range(1, 13)]
plt.figure(figsize=(15,6))
sns.stripplot(x='YEAR', y='MONTH',data=all_times,hue='NARRATIVE',jitter=True, size=7, alpha=0.6, palette=custom_colors)
plt.legend()
plt.title("Dispersion of Narratives on Twitter and FaceBook")
plt.ylabel("Months")
plt.xlabel("Years")

plt.savefig('drive/MyDrive/DisinfoGraphs/all_continuous_chart.jpeg', format='jpeg', bbox_inches='tight', pad_inches=0.2)
plt.show()