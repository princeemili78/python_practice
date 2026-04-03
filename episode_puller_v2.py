import requests
import random
from bs4 import BeautifulSoup



class Episode:
    """Creates episode objects
    :param episode_info: dictionary for each episode from API
    :ivar name: name of episode
    :ivar rating: IMDb rating for episode

    """
    def __init__(self, episode_info, imdb_id):
        self.episode_info = episode_info
        self.imdb_id = imdb_id
        self.season = self.episode_info["season"] if self.check_nulls("season") else "No season info"
        self.number = self.episode_info["number"] if self.check_nulls("number") else "No episode number"
        self.season_and_number = f"S{self.season}E{self.number}"     
        self.name = self.episode_info["name"] if self.check_nulls("name") else "Name not found"
        self.rating = self.episode_info["rating"]["average"] if self.check_nulls("rating", "average") else "No rating found"
        self.type = episode_info["type"] if self.check_nulls("type") else "No type found"
        self.image = episode_info["image"]["medium"] if self.check_nulls("image") and self.check_nulls("image", "medium") else "https://placehold.co/210x295?text=No+Image"
        self.summary = self.get_summary_text() if self.check_nulls("summary") else ""
    
    # Remove HTML tags from episode summary 
    def get_summary_text(self):
        soup = BeautifulSoup(self.episode_info["summary"], "html.parser")
        text = soup.get_text()
        return text
    
    # Check for nulls values so we can handle them differently for the use
    def check_nulls(self, nest_level1, nest_level2=""):
        if nest_level2 == "":
            return self.episode_info[nest_level1] != None 
        else:
            return self.episode_info[nest_level1][nest_level2] != None
        
        

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
        self.imdb_id = self.json["externals"]["imdb"] if self.json["externals"]["imdb"] != None else "No ID found"
        self.picture = self.json["image"]["medium"]
        self.title_id = self.get_title_id()
        self.all_episodes = self.get_all_episodes()
        self.season_list = self.get_season_list()
        



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
        
        return [Episode(e, self.imdb_id) for e in episodes_json]
    
    # Get list of seasons by parsing through episode list for unique season values
    def get_season_list(self):
        season_list = {self.all_episodes[e].season for e in range(len(self.all_episodes))}
        season_list = sorted(season_list)
        return season_list
    
        
# Return random episode 
    def random_episode(self, rating=0, seasons=None):
        if seasons == [] or None:
            seasons = self.season_list


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
    