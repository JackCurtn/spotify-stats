from flask import Flask, render_template, request
import spotify_api


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    artist = ""
    tracks = []
    albums = []
    error = None

    if request.method == "POST":
        artist = (request.form.get("artist") or "").strip()
        if not artist:
            error = "Please enter an artist name."
        else:
            token = spotify_api.get_token()
            if not token:
                error = "Include valid CLIENT_ID and CLIENT_SECRET environment variables."
            else:
                info = spotify_api.search_for_artist(token, artist)
                if not info:
                    error = "Artist not found."
                else:
                    artist_id = info["id"]
                    tracks = spotify_api.get_songs_by_artist(token, artist_id)
                    albums = spotify_api.get_albums_by_artist(token, artist_id)

    return render_template("index.html", artist=artist, tracks=tracks, albums=albums, error=error)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
