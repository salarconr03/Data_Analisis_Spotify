class Playlist:
    def __init__(self, name, n_tracks, playlist_followers, uri=None, description=None, query=None, author=None):
        if not name:
            raise ValueError("name de la playlist es obligatorio.")
        if n_tracks is None:
            raise ValueError("n_tracks (numero de canciones) es obligatorio.")
        if playlist_followers is None:
            raise ValueError("playlist_followers es obligatorio.")

        self.uri = uri
        self.name = str(name)
        self.description = description
        self.query = query
        self.author = author
        self.n_tracks = int(n_tracks)
        self.playlist_followers = int(playlist_followers)