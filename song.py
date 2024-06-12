import json
from bs4 import BeautifulSoup
import requests

client_secret = "eb84a3425fcc432f95c6d2eb90587c4e"  # SPOTIFY CLIENT SECRET
client_id = "640da087c0ce4e18bc752e7bfddf3a98"  # SPOTIFY CLIENT ID

# GENIUS API KEY
genius_api_key = 'OiR_WzY9dAf2ZCqSDhGwIky6hBSQTUqQUnde8-dpmD8eqXyfq6vPF8VH3FMaZ8Ib'


def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(auth_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    response_data = response.json()
    return response_data.get('access_token')


def get_spotify_top_50(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    playlist_id = '37i9dQZEVXbNG2KDcFcKOF'  # Top 50 playlist ID
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tracks_data = response.json().get('items', [])
        tracks_info = []
        for track in tracks_data:
            track_info = track.get('track', {})
            track_id = track_info.get('id')
            track_details = {
                'track_name': track_info.get('name'),
                'artist_name': track_info.get('artists', [{}])[0].get('name'),
                'popularity': track_info.get('popularity'),
                'spotify_url': track_info.get('external_urls', {}).get('spotify', ''),
                'track_id': track_id,
                'album_name': track_info.get('album', {}).get('name', ''),
                'release_date': track_info.get('album', {}).get('release_date', ''),
                'genres': fetch_genres(track_id, access_token)
            }
            tracks_info.append(track_details)
        return tracks_info
    else:
        print(
            f"Failed to fetch tracks: {response.status_code} - {response.text}")
        return []


def fetch_genres(track_id, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        track_data = response.json()
        artist_id = track_data['artists'][0]['id']
        artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=headers)
        if artist_response.status_code == 200:
            artist_data = artist_response.json()
            return artist_data.get('genres', [])
    return []


def get_genius_lyrics(api_key, song_title, artist_name):
    base_url = "https://api.genius.com"
    headers = {'Authorization': f'Bearer {api_key}'}
    search_url = f"{base_url}/search"
    params = {'q': f"{song_title} {artist_name}"}
    response = requests.get(search_url, params=params, headers=headers)
    print(f"Searching for {song_title} by {artist_name}")

    if response.status_code == 200:
        search_results = response.json()['response']['hits']
        for hit in search_results:
            hit_artist = hit['result']['primary_artist']['name'].lower()
            if artist_name.lower() == hit_artist:
                song_url = hit['result']['url']
                print(f"Found URL: {song_url}")
                return fetch_lyrics_page(song_url)
        print("No matching artist found.")
    else:
        print(f"Error fetching song: {response.status_code} - {response.text}")
    return None


def fetch_lyrics_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics_div = soup.find('div', {'data-lyrics-container': 'true'})
        if lyrics_div:
            lyrics = ' '.join([elem.get_text(' ', strip=True) for elem in lyrics_div.find_all(
                ['div', 'a', 'span'], recursive=True) if elem.get_text(strip=True)])
            return lyrics
        print("Lyrics container not found in the expected structure.")
    else:
        print(
            f"Failed to fetch lyrics page: {response.status_code} - {response.text}")
    return None


def fetch_all_lyrics(tracks, genius_api_key):
    all_tracks_with_lyrics = []
    failed_tracks = []

    for track in tracks:
        lyrics = get_genius_lyrics(
            genius_api_key, track['track_name'], track['artist_name'])
        track['lyrics'] = lyrics
        if lyrics:
            all_tracks_with_lyrics.append(track)
        else:
            failed_tracks.append({
                'track_name': track['track_name'],
                'artist_name': track['artist_name'],
                'reason': 'Lyrics not found'
            })
    return {
        'successful_tracks': all_tracks_with_lyrics,
        'failed_tracks': failed_tracks
    }


def save_lyrics_to_json(lyrics_data, filename="lyrics_data.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(lyrics_data, file, ensure_ascii=False, indent=4)


# Main Execution
if __name__ == "__main__":
    access_token = get_access_token(client_id, client_secret)
    top_tracks = get_spotify_top_50(access_token)
    print("TOTAL POPULAR SONGS FROM SPOTIFY: ", len(top_tracks))
    results = fetch_all_lyrics(top_tracks, genius_api_key)

    successful_lyrics = results['successful_tracks']
    failed_lyrics = results['failed_tracks']

    print(f"Successfully fetched lyrics for {len(successful_lyrics)} tracks.")
    if failed_lyrics:
        print("Failed to fetch lyrics for the following tracks:")
        for track in failed_lyrics:
            print(
                f"{track['track_name']} by {track['artist_name']} - {track['reason']}")

    lyrics_data = {
        'successful_tracks': successful_lyrics,
        'failed_tracks': failed_lyrics
    }
    save_lyrics_to_json(lyrics_data)
    print("Lyrics data saved to JSON file.")
