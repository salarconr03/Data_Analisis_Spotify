class Cancion:
    def __init__(self, name, is_playable, artists, playlists, track_uri=None, album_type=None, release_date=None, **kwargs):
        if not name:
            raise ValueError("El nombre de la cancion es obligatorio.")
        if is_playable is None:
            raise ValueError("is_playable es obligatorio.")
        if not artists or len(artists) < 1:
            raise ValueError("Una cancion debe tenr al menos un artista.")
        if not playlists or len(playlists) < 1:
            raise ValueError("Una cancion debe tener al menos una playlist.")

        self.name = str(name)
        self.is_playable = bool(is_playable)
        self.artists = artists
        self.playlists = playlists
        self.track_uri = track_uri
        self.album_type = album_type
        self.release_date = release_date

       
        self.danceability = kwargs.get('danceability')
        self.energy = kwargs.get('energy')
        self.key = kwargs.get('key')
        self.loudness = kwargs.get('loudness')
        self.mode = kwargs.get('mode')
        self.speechiness = kwargs.get('speechiness')
        self.acousticness = kwargs.get('acousticness')
        self.instrumentalness = kwargs.get('instrumentalness')
        self.liveness = kwargs.get('liveness')
        self.valence = kwargs.get('valence')
        self.tempo = kwargs.get('tempo')
        self.duration_ms = kwargs.get('duration_ms')
        self.time_signature = kwargs.get('time_signature')
        
    def total_artistas(self):
        return len(self.artists)
        
    def total_playlists(self):
        return len(self.playlists)