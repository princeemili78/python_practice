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
        self.season = self.set_self("No season info", "season")
        self.number = self.set_self("No episode number", "number")
        self.season_and_number = f"Season {self.season} Episode {self.number}"     
        self.name = self.set_self("No episode name", "name")
        self.rating = self.set_self(0, "rating", "average")
        self.type = self.set_self("No type found", "type")
        self.image = self.set_self("https://placehold.co/210x295?text=No+Image", "image", "medium")
        self.summary = self.get_summary_text() if self.is_null("summary") != True else ""
    # Remove HTML tags from episode summary 
    def get_summary_text(self):
        soup = BeautifulSoup(self.episode_info["summary"], "html.parser")
        text = soup.get_text()
        return text
    
    # Check for nulls values. If value is not null, it returns true
    def is_null(self, nest_level1, nest_level2=""):
        if nest_level2 == "":
            return self.episode_info[nest_level1] == None 
        elif self.episode_info[nest_level1] == None:
            return True
        else:
            return self.episode_info[nest_level1][nest_level2] == None
    
    # Use value for null to return proper value in the init
    def set_self (self, error_value, nest_level1, nest_level2=""):
        if nest_level2 == "":
            if self.is_null(nest_level1) == True:
                return error_value
            else:
                return self.episode_info[nest_level1]
        else:
            if self.is_null(nest_level1, nest_level2) == True:
                return error_value
            else:
                return self.episode_info[nest_level1][nest_level2] 

        
        
        

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
    

# Create list of episodes that satisfy seasons and rating requirements
    def valid_episodes(self, rating=0, seasons=None):
        if seasons == [] or seasons == None:
            seasons = self.season_list
        if rating == None:
            rating = 0


        # Create list of episodes that satisfy the user's requirements by filtering with a list comprehension
        valid_episodes = [e for e in self.all_episodes if e.rating != None and e.season in seasons and e.rating >= rating]
        if len(valid_episodes) == 0:
            raise Exception("Ur rating is too high fuck nigga, lower ur standards")
        else:
            return valid_episodes
# Return random episode 
    def random_episode(self, valid_episodes):
        if valid_episodes != []:      
            random_episode = random.choice(valid_episodes)
            return random_episode
        else:
            raise Exception ("No more random episodes")
        


# Function to return the name of the first result in a search
def fuzzy_search_result(typo):
    r = requests.get(f"https://api.tvmaze.com/search/shows?q= {typo}").json()
    if r == None:
            raise Exception("Could not find a show with that name")
    
    top_result_name = r[0]["show"]["name"]  
    return top_result_name 
    