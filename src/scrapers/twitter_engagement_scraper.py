import asyncio
import json
from twscrape import API, gather
from twscrape.logger import set_log_level



accounts = [
    "Libsoftiktok",
'EndWokeness',
'AmiriKing',
'Visegrad24',
'MattWallace888',
'CollinRugg',
'4Mischief',
'SaraGonzalesTX',
'Robbystarbuck',
'MJTruthUltra',
'ClayTravis',
'SteveGuest',
'Liz_Wheeler',
'Megynkelly',
'Charliekirk11',
'MattWalshShow',
'Scarlett4kids',
'Megbasham',
'DameScorpio',
'Teagan1776',
'DrLoupis',
'Glennbeck',
'iheartmindy',
]

narratives = {
    'lakewood': { 'start-date': "2024-02-01", 'keywords':"Lakewood Church shooter transgender"
    }, 
    'tampons':{ 'start-date': '2024-07-01', 'keywords':"tampons in boy's restrooms"

    },
    'target':{ 'start-date': '2023-04-01', 'keywords':"tuck-friendly bathing suits"

    }
}


async def main():
    # or API("path-to.db") - default is `accounts.db`
    api = API()
    # ADD ACCOUNTS (for CLI usage see BELOW)
    await api.pool.add_account("lillie71961", "l1ll13sw0rd", "lillieayer@gmail.com", "pda.3690", cookies="ct0=e3277716253b1bd1fe069b46ee40d248986de246917eecafae57e4ad73275b1b0ba3fb53de2b42ffdadcda8a6caf6cf5ea9ea630142cae11577d4b6657dfc1f1c44887553caf84ddc905adf511c4aced")
    await api.pool.add_account("laayer119311", "pda.3690", "laayer@wm.edu", "Pda.3690", cookies="ct0=ae4dbe560cbd0aa760c31bc9368c3c907356ecf433c4325c21f20ec5707ca7a73fee5f81564984e1e99a3ede44f7ebbc511d89afed589e328e446ac732c8901b20f4b43f325235c31b7b52c7fd8af2f3")
    # API USAGE

    query = "Lakewood Church shooter transgender since:" + narratives['lakewood']['start-date'] 
    tweets = await gather(api.search(query))

    with open('./output/rapid_continuous/twitter/test.json', 'w', encoding='utf-8') as testfile:
        json.dump(tweets, testfile, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    asyncio.run(main())
