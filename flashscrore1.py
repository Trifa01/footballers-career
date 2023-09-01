import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents

# Get squadstable


teams_data = requests.get("https://s.livesport.services/api/v2/search/?q=football&lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1&sport-ids=1").json()

league_url ="https://www.flashscore.com/football/france/ligue-1/#/Q1sSPOn5/table/overall"
response= requests.get(league_url) 
league_soup = BeautifulSoup(response.text, 'html.parser')

team_url = "https://www.flashscore.com/football/france/ligue-1/#/Q1sSPOn5/table/overall"

for team in teams_data:

    team_id = team["id"]
    team_name = team["url"]

    print(team_name)

    # get the response in the form of html
    url=f"https://www.flashscore.com/team/{team_name}/{team_id}/squad/"
    player_class ="lineup__cell lineup__cell--name"
    response=requests.get(url) 

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    player_list = soup.find_all('div',{'class':"lineup__cell--nameAndAbsence"})
 
    data = []
    for i in range(len(player_list)):
        player_url = player_list[i].find('a', href=True) ["href"]
        player_id = player_url.split("/")[-2]
        player_name = player_url.split("/")[-3]

        player_url_full = f"https://www.flashscore.com/player/{player_name}/{player_id}/"
        player_reponse = requests.get(player_url_full)
        player_soup = BeautifulSoup(player_reponse.text, 'html.parser')

        player_name_full = player_soup.find_all("div", {"class":"heading__name"})[0].text
        player_position = player_soup.find_all("div", {"class":"heading__info--type-name"})[0].text

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

        data.append({"player":player_name_full, "position":player_position,"flashscore_url":player_url_full, "seasons":seasons, "teams":teams, "transfers":transfers, "logos":logos}) 
        print(player_url_full)
        print('end player')

    df = pd.DataFrame(data)
    df.to_csv(f"{team_name}.csv", index=False, sep=";")
print("end")

# Find squads 
# https://s.livesport.services/api/v2/search/?q=football&lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1&sport-ids=1

# Got to squad 

# https://www.flashscore.com/team/paris-sg/CjhkPw0k/squad/


# # /player/donnarumma-gianluigi/WScbdXmL/  
# https://s.livesport.services/api/v2/search/?q=ronaldo&lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1 


# indiatable=soup.find('table',{'class':"wikitable"})
# https://s.livesport.services/api/v2/top-search/?lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1&limit=10



            #######

            # season_list = [x.text for x in player_soup.find_all("div", {'class':"careerTab__season"})]
            # if season_list:
            #     team_list = [x.text for x in player_soup.find_all("a", {'class':"careerTab__competitionHref"}) if x["href"].startswith("/team")]
            #     logo_list = [x["src"] for x in player_soup.find_all("img", {'class':"careerTab__logo"})]
            #     try:
            #         # LIMIT TO THE LEAUGE VIEW 
            #         LIMIT_LEAGUE_VIEW = season_list[1:].index("Season")
            #     except ValueError as ve:
            #         LIMIT_LEAGUE_VIEW = len(season_list)
                
            #     season_list = season_list[1:LIMIT_LEAGUE_VIEW+1]
            #     # team_list = [(team_list[i], team_list[i+1]) for i in range(len(team_list)-1)][1:LIMIT_LEAGUE_VIEW+1]
            #     team_list = team_list[0:LIMIT_LEAGUE_VIEW]
            #     logo_list = logo_list[0:LIMIT_LEAGUE_VIEW]
            #     assert((len(logo_list) == len(season_list)) and (len(team_list)==len(season_list)))

            #     data.append({"player":player_name, "flashscore_url":player_url_full, "transfer_date_from":transfer_dates_from, "transfer_date_to":transfer_dates_to, "transfer_from":transfer_teams_from, "transfer_to":transfer_teams_to, "season":season_list,"team":team_list, "logo":logo_list}) 
            #     print(player_url_full)
            #     print('end player')


                        #transfer_logos = [x.find("image")["href"] for x in player_soup.find_all("svg", {'class':"transferTab__teamLogo"})]
            #transfer_logos_from = [transfer_logos[i] for i in range(0, len(transfer_logos),2)] # Even indexes
            #transfer_logos_to = [transfer_logos[i] for i in range(0, len(transfer_logos)) if i % 2 ] # Odd indexes
            # logos2 = transfer_logos_to + [transfer_logos_from[-1]]