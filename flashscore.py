import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

urls_df = pd.read_csv("data/urls.csv")

data = []
for _,row in urls_df.iterrows():

    player_reponse = requests.get(row['url'])
    player_soup = BeautifulSoup(player_reponse.text, 'html.parser')

    player_name_full = player_soup.find_all("div", {"class":"heading__name"})[0].text
    player_position = player_soup.find_all("div", {"class":"heading__info--type-name"})[0].text
    try:
        player_nationality = player_soup.find_all("a", {"class":"breadcrumb__link"})[1].text
    except:
        player_nationality = ""
    player_photo = player_soup.find_all("img", {'class':"heading__logo heading__logo--1"})[0]["src"]

    # Transfers 
    seasons = []
    teams = []
    transfers = []
    logos = []
    
    transfer_dates = [x.text for x in player_soup.find_all("div", {'class':"transferTab__date"})][1:]
    
    if transfer_dates:
        transfer_dates_from = transfer_dates + ["-"]
        transfer_dates_to = ["-"] + transfer_dates 
        seasons = list(zip(transfer_dates_from, transfer_dates_to))
        
        transfer_teams = [x.text for x in player_soup.find_all("a", {'class':'transferTab__teamHref'})]
        transfer_teams_from = [transfer_teams[i] for i in range(0, len(transfer_teams),2)] # Even indexes
        transfer_teams_to = [transfer_teams[i] for i in range(0, len(transfer_teams)) if i % 2 ] # Odd indexes
        teams = transfer_teams_to + [transfer_teams_from[-1]]

        transfer_logos = [x.find("image")["href"] for x in player_soup.find_all("svg", {'class':"transferTab__teamLogo"})]
        transfer_logos_from = [transfer_logos[i] for i in range(0, len(transfer_logos),2)] # Even indexes
        transfer_logos_to = [transfer_logos[i] for i in range(0, len(transfer_logos)) if i % 2 ] # Odd indexes
        logos = transfer_logos_to + [transfer_logos_from[-1]]

        transfers = [x.text.strip() for x in player_soup.find_all("div", {'class':'transferTab__typeText'})] + ["-"]

        assert(len(teams)==len(seasons)==len(transfers)==len(logos))

    data.append({"player":player_name_full, "position":player_position,"nationality":player_nationality, "photo":player_photo, "flashscore_url":row["url"], "seasons":seasons, "teams":teams, "transfers":transfers, "logos":logos}) 
    print(row["url"])
    print('end player')

df = pd.DataFrame(data)
df.to_csv(f"players.csv", index=False, sep=";")
print("end")