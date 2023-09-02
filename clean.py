# read all csv
# player,flashscore_url,transfer_date,transfer_from,transfer_to,logo_from,logo_to

# Import libraries
import glob
import pandas as pd

# Get CSV files list from a folder
csv_files = glob.glob("players.csv")

# Read each CSV file into DataFrame
# This creates a list of dataframes
df_list = (pd.read_csv(file, sep=";"
                       , converters={
                           'seasons': pd.eval,
                           'teams': pd.eval, 
                           'transfers': pd.eval,
                           'logos': pd.eval,
                                     }
                       ) for file in csv_files)

# Concatenate all DataFrames
big_df   = (pd.concat(df_list, ignore_index=True)
            .drop_duplicates(subset=["player"])
            )

# Position 
big_df["position"] = big_df["position"].apply(lambda x:"".join(ch for ch in str(x).split("(")[0] if ch.isalnum()))

# Create first and last name (jay jay okocha -> Jay jay | Okocha, )
big_df["last_name"] = big_df["player"].apply(lambda x:str(x).split(" ")[-1].capitalize())
big_df["first_name"] = big_df["player"].apply(lambda x:" ".join(str(x).split(" ")[:-1]).capitalize())

# Handle slashes in url
big_df['flashscore_url'] = big_df['flashscore_url'].str.replace('/', '___SLASH___')


all_df = (big_df[["first_name","last_name", "position", "nationality", "photo", "flashscore_url", "seasons", "teams", "transfers", "logos"]]
          .explode(["seasons", "teams", "transfers", "logos"])
          )

all_df['logos'] = all_df['logos'].str.replace('/', '___SLASH___')
all_df['photo'] = all_df['photo'].str.replace('/', '___SLASH___')

all_df = all_df[~all_df.teams.isnull()]

all_df["seasons"] = all_df.apply(lambda x:(str(x['seasons'][0]).split(".")[-1], str(x['seasons'][1]).split(".")[-1]), axis=1)

all_df["teams"] = all_df.apply(lambda x:{"name":x["teams"], "season":x["seasons"], "transfer":x["transfers"], "logo":x["logos"]}, axis=1)

final_df = all_df.groupby(["first_name","last_name", "position", "nationality", "photo", "flashscore_url"])["teams"].apply(list).reset_index()

json_output = final_df.to_json(orient="records", indent=1, force_ascii=False)

json_output = json_output.replace('___SLASH___', '/')

with open("players.json", 'w') as f:
    f.write(json_output)
print(final_df.count())

print("end")
## Format des données

# ```python
# [
#     {
#         "player": "MESSI",  # Peut importe la casse
#         "nationality": "Argentina",  # Peut importe la casse
#         "birth_year": "1987",
#         "teams": [
#             {"name": "Barcelona", "season": "2004-2005"},
#             {"name": "Barcelona", "season": "2005-2006"},
#             # ...
#         ],
#     },
#     {
#         "player": "CRISTIANO RONALDO",  # Peut importe la casse
#         "nationality": "Portugal",  # Peut importe la casse
#         "birth_year": "1987",
#         "teams": [
#             # ...
#             {"name": "Real Madrid", "season": "2011-2012"},
#             {"name": "Real Madrid", "season": "2012-2013"},
#             # ...
#         ],
#     },
# ]
# ```
