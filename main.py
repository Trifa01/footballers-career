import wikipediaapi
import pandas as pd 

wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')


fifa100_df = pd.read_csv("fifa100.csv")

data = []
for _,row in fifa100_df.iterrows(): 
    player = row["Player"]
    page = wiki_wiki.page(player)
    print("Page - Exists: %s" % page.exists())
    clubs = []
    if page.exists():
        print("Page - Title: %s" % page.title)
        # Page - Title: Python (programming language)
        print("Page - Summary: %s" % page.summary[0:60])
        # Page - Summary: Python is a widely used high-level programming language for
        if page.section_by_title('Club career'):
            for club in page.section_by_title('Club career').sections:
                clubs.append(club.title)
            if len(clubs) > 0:
                data.append({'player':player, 'career':clubs, 'position':row["Position"], 'born':row["Born"], 'died':row["Died"]})

# print("Career", page.section_by_title('Club career'))
df = pd.DataFrame(data)
df.to_csv("careers.csv", index=False)
print("end file")