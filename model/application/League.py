from model.application import Team
from model.exception.UnauthorisedAccessException import UnauthorisedAccessException
from model.utils.SeedData import seeded_data
from model.application.Teams import Teams
from model.exception.InvalidSigningException import InvalidSigningException


class League:
    def __init__(self, seeded_teams, seeded_players, seeded_managers):
        self.teams = seeded_teams
        self.manageable_teams = Teams([team for team in self.teams.get_teams() if team.get_manager() is None])
        self.players = seeded_players
        self.managers = seeded_managers
        self.logged_in_manager = None

    def get_teams(self):
        return self.teams

    def get_manageable_teams(self):
        return self.manageable_teams

    def get_players(self):
        return self.players

    def get_logged_in_manager(self):
        return self.logged_in_manager

    def set_logged_in_manager(self, manager):
        self.logged_in_manager = manager

    def set_manager_for_team(self, manager, team):
       
        if manager is None or team is None:
            raise Exception("Team and Manager cannot be null")
        if team.get_manager() is not None:
            raise Exception("Team already has a Manager. You should only be calling this method on a Team that is in the manageableTeams list")
        if manager.get_team() is not None:
            old_team = manager.get_team()
            old_team.set_manager(None)
            self.manageable_teams.add(old_team)
        manager.assign_team(team)
        team.set_manager(manager)
        self.manageable_teams.remove(team)

    def withdraw_manager_from_team(self, manager):
       
        if manager is None:
            raise Exception("Manager cannot be null")
        if manager.get_team() is None:
            raise Exception("Manager is not assigned to any team")
        self.manageable_teams.add(manager.get_team())
        manager.get_team().set_manager(None)
        manager.assign_team(None)

    def validate_manager(self, id):
        
        try:
            id = int(id)
        except (ValueError, TypeError):
            raise UnauthorisedAccessException("Incorrect format for manager id")
        
        for manager in self.managers:
            if manager.has_id(id):
                return manager
        raise UnauthorisedAccessException("Invalid login credentials")
    
    def sign_player_to_team(self, player_name, team):
        player = self.players.player(player_name)
        
        if player is None:
            raise InvalidSigningException(f"Player {player_name} does not exist within the league.")
        
        if player.get_team() is not None:
            if player.get_team() == team:
                raise InvalidSigningException(f"Player {player_name} is already signed to your team.")
            else:
                raise InvalidSigningException(f"Cannot sign {player_name}, player is already signed to {str(player.get_team())}")
        
        team.add_player(player)
        player.set_team(team)
    
    

league = League(seeded_data.get_teams(), seeded_data.get_players(), seeded_data.get_managers())
