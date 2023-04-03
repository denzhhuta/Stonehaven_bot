import mcrcon

# Replace "SERVER_IP" and "RCON_PASSWORD" with your server IP and RCON password
with mcrcon.MCRcon("SERVER_IP", "RCON_PASSWORD") as rcon:
    response = rcon.command("list")
    # Extract the player count from the response string
    player_count = response.split(":")[1].split("/")[0].strip()
    print("There are", player_count, "players online.")
