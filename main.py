from requests import get, post
import json
import os

token = os.getenv("ACCESS_TOKEN")
print(f"{token = }")

# def user_autherization():
#     url = "https://accounts.spotify.com/authorize"
#     query = {
#         "client_id": client_id,
#         "response_type": "code",
#         "redirect_uri": "http://localhost:8080",
#         "scope": "user-read-private user-read-email"
#     }
#     result = get(url, params=query)
#     print(result.url)

# user_autherization()
# quit()


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name, limit=1):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit={limit}"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    artists = []
    for item in json_result:
        artist_name = item["name"]
        uri = item["uri"]
        followers = item["followers"]["total"]
        genres = item["genres"]
        artists += artist_name
        
        print(f"{artist_name = }".ljust(40), end='')
        print(f"{followers = }".ljust(25), end='')
        print(f"{uri = }".ljust(55), end='')
        print(f"{genres = }")
        
    # print(json.dumps(json_result, indent=4), sep='\n')
    
    if len(json_result) == 0:
        print("No such artist exists...")

def search_for_playlist(token, playlist_name, limit=1):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={playlist_name}&type=playlist&limit={limit}"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    for item in json_result:
        name = item["name"]
        owner = item["owner"]["display_name"]
        uri = item["uri"]
        
        print(f"{owner = }".ljust(45, " "), end='')
        print(f"playlist {name = }".ljust(60, " "), end='')
        print(f"{uri = }")
        
    # print(json.dumps(json_result, indent=4))
    return json_result

def get_songs_by_artist(token, artist_name, limit=5):
    def get_artist_id(artist_name, limit=1):
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = f"q={artist_name}&type=artist&limit={limit}"
        query_url = url + "?" + query
        
        result = get(query_url, headers=headers)
        if result.status_code != 401:
            json_result = json.loads(result.content)["artists"]["items"]
            print(f"{json_result = }")
            
            id = json_result[0]["id"]
            print(f"{artist_name = }, {id = }")
            return id
        else:
            json_result = json.loads(result.content)
            print(json_result)
        
    artist_id = get_artist_id(artist_name) 
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US&limit={limit}"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    print(json.dumps(json_result, indent=4))
    return json_result

def get_user_saved_albums(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_auth_header(token)
    print(headers)
    result = get(url, headers=headers)
    print(result)
    json_result = json.loads(result.content)
    print(json.dumps(json_result, indent=4))


# result = search_for_artist(token, "eminem", 10)

# result = search_for_playlist(token, "Best songs 2024", 25)

# result = get_songs_by_artist(token, "eminem")

# artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
for i, song in enumerate(songs):
    print(f"{i+1}. {song['name']}")

# result = search_for_playlist(token, "pop")
# for i, playlist in enumerate(result):
#     print(f"{i}. {playlist['external_urls'][w'spotify']} \t  total: {playlist['tracks']['total']} \t {playlist['name']}")

# get_user_saved_albums(token)