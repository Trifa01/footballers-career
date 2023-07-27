# Football career Quiz with Excel
Guess the player based on his club career

## Try the Quiz
All you need to do is download the Excel file [foot_career_quiz](./foot_career_quiz.xlsx)

## How to play ?
1. Press **F9** to load a career
2. Guess the player from the dropdown list
3. Press **Shift+F9** to check 
4. Try it all again


# How I get the data
I am using
- **Wikipedia-API:** an easy to use Python wrapper for Wikipedias’ API
- **requests:** to handle requests
- **BeautifulSoup:** to parse HTML documents

1. A list of players from the [fifa100](https://en.wikipedia.org/wiki/FIFA_100)
2. For each player:
    - I get the Wiki page 
    - Parse the section "Club Career"
3. Put it all together in a dataframe with other infos like Position and the birth year   


# 