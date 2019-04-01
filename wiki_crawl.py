## The point of this script is to crawl the
## Wiki located at
## https://southpark.fandom.com/

import requests
import json
import bs4
import re
import sys

# Step one, grab the list of seasons from
# https://southpark.fandom.com/wiki/Portal:Scripts
script_dir = requests.get('https://southpark.fandom.com/wiki/Portal:Scripts')
script_dir_data = script_dir.text
season_re_string = '.wiki.Season_(\w+)'
seasons = set(re.findall(season_re_string, script_dir_data))
print(seasons)

# Step two, for each season grab the list of episodes from
# https://southpark.fandom.com/wiki/Portal:Scripts/Season_Five
season_episodes = {}
for season in seasons:
    season_dir = requests.get("https://southpark.fandom.com/wiki/Portal:Scripts/Season_"+season)
    season_dir_data = season_dir.text
    episode_re_string = '.wiki.(\w+)\/Sc'
    episodes = set(re.findall(episode_re_string, season_dir_data))
    season_episodes[season] = episodes

print(season_episodes)

# Step Three, for each episode grab the script data
# https://southpark.fandom.com/wiki/Terrance_and_Phillip:_Behind_the_Blow/Script
script = ''
for season in season_episodes:
    print("\nSeason : "+ season)
    for episode in season_episodes[season]:
        sys.stdout.write("\rEpisode " +episode)
        sys.stdout.flush()
        episode_dir = requests.get("https://southpark.fandom.com/wiki/"+episode+"/Script")
        soup = bs4.BeautifulSoup(episode_dir.text, 'html.parser')
        for center_tag in soup.find_all('tr'):
            for character in center_tag.find_all('center'):
                script += center_tag.text

scriptfile = open('script_text.txt','w', encoding='utf-8')
scriptfile.write(script)
scriptfile.close()
