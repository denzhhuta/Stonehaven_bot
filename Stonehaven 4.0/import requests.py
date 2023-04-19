import requests

ip_address = "193.169.195.76" # replace with your Minecraft server IP address
port = 25565 # replace with your Minecraft server port

# Replace "player_username" with the username of the player you want to check
player_username = "morkovka"

# Query the API to get player information
player_url = f"https://api.mcsrvstat.us/2/{ip_address}:{port}/player/{player_username}"
response = requests.get(player_url)

if response.status_code == 200:
    data = response.json()
    print(response)
    if data["online"]:
        print(f"{player_username} is online.")
    else:
        print(f"{player_username} is offline.")
else:
    print(f"Error: {response.status_code}")