import requests
import random
from bs4 import BeautifulSoup



class Episode:
    """Creates episode objects
    :param episode_info: dictionary for each episode from API
    :ivar name: name of episode
    :ivar rating: IMDb rating for episode

    """
    def __init__(self, episode_info):
        self.episode_info = episode_info
        self.season_and_number = f"S{self.episode_info["season"]}E{self.episode_info["number"]}"
        self.season = self.episode_info["season"]
        self.name = self.episode_info["name"]
        self.rating = self.episode_info["rating"]["average"]
        self.type = episode_info["type"]
        self.image = episode_info["image"]["medium"]
        self.summary = self.get_summary_text()
    
    # Remove HTML tags from episode summary 
    def get_summary_text(self):
        soup = BeautifulSoup(self.episode_info["summary"])
        text = soup.get_text()
        return text
        

class TvShow:
    """Creates instance of TV show you want to watch

    :param show_name: title of the TV show
    :ivar show_json: json for entire show returned
    :ivar title_id: ID for show on TVAPI
    :ivar seasons: List of seasons object corresponding to number of seasons in show
    """

    def __init__(self, name):
        self.name = name
        self.json = self.get_json()
        self.picture = self.json["image"]["medium"]
        self.title_id = self.get_title_id()
        self.all_episodes = self.get_all_episodes()
        self.num_seasons = self.all_episodes[-1].season



# Add string for show name to the end of the api address to show json  
    def get_json(self):
        r = requests.get("https://api.tvmaze.com/singlesearch/shows?q=" + self.name)
        if r.json() == None:
            raise Exception("Could not find a show with that name")
        
        return r.json()
    
    def get_title_id(self):
        id = self.json["id"]
        return id


    def get_all_episodes(self):
        episodes_json = requests.get(f"https://api.tvmaze.com/shows/{self.title_id}/episodes").json()
        
        return [Episode(e) for e in episodes_json]
        
# Return random episode 
    def random_episode(self, rating=0, seasons=None):
        if seasons is None:
            seasons = [num for num in range(self.num_seasons)]

        # Create list of episodes that satisfy the user's requirements by filtering with a list comprehension
        valid_episodes = [e for e in self.all_episodes if e.rating != None and e.season in seasons]
        if len(valid_episodes) == 0:
            return "Ur rating is too high fuck nigga, lower ur standards"
        random_episode = random.choice(valid_episodes)

        
        return random_episode
        


# Function to return the name of the first result in a search
def fuzzy_search_result(typo):
    r = requests.get(f"https://api.tvmaze.com/search/shows?q= {typo}").json()
    if r == None:
            raise Exception("Could not find a show with that name")
    
    top_result_name = r[0]["show"]["name"]  
    return top_result_name 
    