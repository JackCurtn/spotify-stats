import spotify_api


def main():
	artist = input("Enter artist name: ").strip()
	token = spotify_api.get_token()
	result = spotify_api.search_for_artist(token, artist)

	if not result:
		return

	artist_id = result["id"]

	songs = spotify_api.get_songs_by_artist(token, artist_id)
	albums = spotify_api.get_albums_by_artist(token, artist_id)

	print("Top Songs:")
	for idx, song in enumerate(songs):
		print(f"{idx + 1}. {song['name']}")

	print("\nAlbums:")
	for idx, album in enumerate(albums):
		print(f"{album['release_date'][:4]} - {album['name']}")


if __name__ == "__main__":
	main()
	