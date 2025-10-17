from model.exception.FillException import FillException
from model.exception.InvalidSigningException import InvalidSigningException
class Team:
    REQUIRED_TEAM_SIZE = 5

    def __init__(self, local_name, team_name, manager, all_players):
        self.local_name = local_name
        self.team_name = team_name
        self.manager = manager
        self.all_players = all_players
        self.current_team = []
        for i in range(Team.REQUIRED_TEAM_SIZE):
            self.current_team.append(None)

    def get_team_name(self):
        return self.team_name

    def get_manager(self):
        return self.manager

    def set_manager(self, manager):
        self.manager = manager

    def get_all_players(self):
        return self.all_players
    
    def get_current_team(self): 
        return self.current_team
    
    def add_player(self, player):
        if player not in self.all_players.get_players():
            self.all_players.add(player)

    def remove_player(self, player):
        if self.is_player_in_active_team(player):
            raise InvalidSigningException("Player is in the active team and cannot be unsigned.")
        self.all_players.remove(player)
        player.set_team(None)

    def is_player_in_active_team(self, player):
        return player in self.current_team

    def assign_player_to_position(self, player, position_index):
        try:
            current_position_of_player = self.current_team.index(player)
        except ValueError:
            current_position_of_player = None 

        player_at_destination = self.current_team[position_index]

       
        if current_position_of_player is not None and player_at_destination is None:
            player_name = player.get_full_name()
            raise FillException(f"{player_name} is already in the active playing team.")
        
       
        if current_position_of_player is None:
            self.current_team[position_index] = player
     

    def unassign_player_from_position(self, position_index):
        self.current_team[position_index] = None


    def __str__(self):
        return self.local_name + " " + self.team_name
    
    def get_jersey_filename(self):
        return f"{self.team_name.lower()}.png"