from nhlpy import NHLClient
from datetime import datetime

class Scraper():
    def __init__(self, date: str = datetime.today().strftime('%Y-%m-%d')):
        self.client = NHLClient()
        self.day: str = date
        self.schedule_metadata: dict = self.client.schedule.get_schedule(date=date).get('games') # dict of schedule information
        self.num_games: int = len(self.schedule_metadata) # number of games for today's date
        self.schedule: list[dict] = []
        
    def get_schedule_metadata(self) -> dict:
        return(self.schedule_metadata)
    
    def get_num_games(self) -> int:
        return(self.num_games)
    
    def __get_schedule(self) -> dict:
        return(self.schedule)
    
    def parse_single_game_data(self, game_data: dict) -> dict:
        """
            Gets required data (for GUI) for a game in the schedule metadata
            Retrieves team names, logos, and match time information for a game.

            Returns:
                dict: Dictionary containing required data for a game
        """
        
        name_away_team: str = game_data.get('awayTeam').get('placeName')['default'].lower()
        name_home_team: str = game_data.get('homeTeam').get('placeName')['default'].lower()
        logo_away_team: str = game_data.get('awayTeam').get('logo')
        logo_home_team: str = game_data.get('homeTeam').get('logo')

            
        game_data: dict = {
                            "away_team": {"city": name_away_team, "logo": logo_away_team},
                            "home_team": {"city": name_home_team, "logo": logo_home_team},
                          }
        
        return game_data
    
    def build_schedule(self) -> list[dict]:
        """
            Adds each game's parsed data as a dict and builds proper schedule data.
        """
        
        schedule: list = []
        
        try:      
            for game in self.schedule_metadata:
                game_i: dict = game
                
                game_data = self.parse_single_game_data(game_i)
                
                schedule.append(game_data)
        except IndexError:
            raise IndexError(f'No games today: {self.day}')
            
        return schedule
    
    def set_schedule(self) -> None:
        """Sets schedule with finalized data for each game.
        """
        self.schedule = self.build_schedule()
        
    def nhl_schedule(self) -> list[dict]:
        """Returns the finalized daily schedule lsit of dictionaries of finalized match data for the GUI.

        Returns:
            list[dict]: List of dicts with finalized data for each game.
        """
        self.set_schedule()
        return(self.__get_schedule())