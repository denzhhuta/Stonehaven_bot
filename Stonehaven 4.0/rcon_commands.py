import mcrcon

host = "127.0.0.1"
port = 25508
PASSWORD = "NnypReh2KR8tMnNy"

def ban_player(player_name: str, reason: str):
    with mcrcon.MCRcon(host, PASSWORD, port) as rcon:
        response = rcon.command(f"ban {player_name} {reason}")
        return response
        
def kick_player(player_name: str, reason: str):
    with mcrcon.MCRcon(host, PASSWORD, port) as rcon:
        response = rcon.command(f"kick {player_name} {reason}")
        return response 

def player_announce(announce_message: str):
     with mcrcon.MCRcon(host, PASSWORD, port) as rcon:
        response = rcon.command(f"say {announce_message}")
        return response 

#def restart_server()