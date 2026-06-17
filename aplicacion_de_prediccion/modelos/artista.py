class Artista:
    def __init__(self, artist_popularity, artist_genres, artist_followers, artist_uri=None):
        if artist_popularity is None:
            raise ValueError("artist_popularity es obligatorio.")
        

        if isinstance(artist_genres, str):
            generos_limpios = [g.strip() for g in artist_genres.split(',') if g.strip()]
        elif isinstance(artist_genres, list):
            generos_limpios = [str(g).strip() for g in artist_genres if str(g).strip()]
        else:
            generos_limpios = []
            
        if not generos_limpios:
            raise ValueError("Un artista debe tener al menos un genero (artist_genres).")
            
        if artist_followers is None:
            raise ValueError("artist_followers es obligatorio.")

        self.artist_uri = artist_uri
        self.artist_popularity = int(artist_popularity)
        self.artist_genres = generos_limpios
        self.artist_followers = int(artist_followers)