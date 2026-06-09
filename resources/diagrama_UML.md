```mermaid
---
config:
  layout: elk
---
classDiagram

class Artista {
    artist_uri: str
    artist_popularity: int
    artist_genres: list<st>
    artist_followers: int

}

class Cancion {
    track_uri: str
    name: str
    album_type: str
    is_playable: bool
    release_date: date

    artists_uris: list<string>
    artists_names: list<artista>
    artists_popularities: list<int>
    artists_genres: list<list<string>>
    artists_followers: list<int>

    playlist_uris: list<str>

    popularity: int
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int

    metodo_lol()
}


class Playlist {
    uri: str
    name: str
    description: str
    query: str
    author: str
    n_tracks: int
    playlist_followers: int

}


Cancion o-- "*" Artista : es interpretada por
Playlist o-- "*" Cancion : contiene

Artista "*" -- "*" Playlist : aparece en

