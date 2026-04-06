from dotenv import load_dotenv
import base64
import os
from requests import get, post


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    """Retrieves an access token from the Spotify Accounts service.

    Args:
        client_id: Client ID provided by Spotify.
        client_secret: Client secret provided by Spotify.

    Returns:
        The access token string if successful, otherwise None.
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    return result.json().get("access_token")


def get_auth_header(token):
    """Constructs the authorization header for Spotify API requests.

    Args:
        token: Spotify access token.

    Returns:
        A dictionary containing the Bearer Authorization header.
    """
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    """Searches for an artist by name.

    Args:
        token: Spotify access token.
        artist_name: Name of the artist to search for.

    Returns:
        A dictionary containing artist data if found, otherwise None.
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = result.json()["artists"]["items"]
    if len(json_result) == 0:
        print("Not found")
        return None
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    """Retrieves top tracks for a specific artist.

    Args:
        token: Spotify access token.
        artist_id: Spotify ID of the artist.

    Returns:
        A list of dictionaries representing top tracks.
    """
    url = (
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    )
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return result.json()[
        "tracks"
    ]


def get_albums_by_artist(token, artist_id, include_groups="album", market="US", limit=50):
    """Retrieves a list of albums for a specific artist.

    Args:
        token: Spotify access token.
        artist_id: Spotify ID for the artist.
        include_groups: Comma-separated list of keywords (e.g., 'album', 'single').
        market: Xountry code.
        limit: Maximum number of items to return.

    Returns:
        A list of dictionaries representing the artist's albums.
    """
    url = (
        f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    )
    headers = get_auth_header(token)
    params = {
        "include_groups": include_groups,
        "market": market,
        "limit": limit,
    }
    result = get(
        url,
        headers=headers,
        params=params,
    )
    return result.json().get("items", [])
