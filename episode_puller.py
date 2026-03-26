import requests
import pandas as pd

class TvShow:
    """Creates instance of TV show you want to watch

    :param title: title of the TV show
    """

    def __init__(self, show_name):
        self.show_name = show_name
        self.title_id = self.pull_title_id()



# Add string for show name to the end of the api address to pull the ID    
    def pull_title_id(self):
        r = requests.get("https://api.tvmaze.com/singlesearch/shows?q=" + self.show_name)
        
        return r.json()["id"]

        


