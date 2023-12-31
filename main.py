import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# print(get_token())
# quit()


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No such artist exists...")
        return None

    return json_result[0]

    print(json.dumps(json_result, indent=4))

def search_for_playlist(token, playlist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={playlist_name}&type=playlist&limit=10"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    print(json.dumps(json_result, indent=4))
    return json_result



def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_user_saved_albums(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_auth_header(token)
    print(headers)
    result = get(url, headers=headers)
    print(result)
    json_result = json.loads(result.content)
    print(json.dumps(json_result, indent=4))

token = os.getenv("ACCESS_TOKEN")
result = search_for_artist(token, "eminem")
print(result["name"])

# artist_id = result["id"]
# songs = get_songs_ny_artist(token, artist_id)
# for i, song in enumerate(songs):
#     print(f"{i+1}. {song['name']}")

# result = search_for_playlist(token, "pop")
# for i, playlist in enumerate(result):
#     print(f"{i}. {playlist['external_urls'][w'spotify']} \t  total: {playlist['tracks']['total']} \t {playlist['name']}")

get_user_saved_albums(token)