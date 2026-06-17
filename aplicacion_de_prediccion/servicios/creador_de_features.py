# servicios/creador_de_features.py

class CreadorDeFeatures:
    """Se encarga exclusivamente de calcular las metricas derivadas y construir el vector q se le va a pasar al modelo ouyea."""
    
    def procesar(self, cancion):
        num_artistas = cancion.total_artistas()
    
        pop_media_artistas = sum(a.artist_popularity for a in cancion.artists) / num_artistas
        
        num_medio_generos_artistas = sum(len(a.artist_genres) for a in cancion.artists) / num_artistas
        
        seg_medios_artistas = sum(a.artist_followers for a in cancion.artists) / num_artistas
        
        num_playlists = cancion.total_playlists()
        num_medio_canciones_pl = sum(p.n_tracks for p in cancion.playlists) / num_playlists
        seg_medios_pl = sum(p.playlist_followers for p in cancion.playlists) / num_playlists
        
        vector_final = [
            num_artistas,
            pop_media_artistas,
            num_medio_generos_artistas,
            seg_medios_artistas,
            num_medio_canciones_pl,
            seg_medios_pl
        ]
        
        metricas_resumen = {
            "Artistas Involucrados": num_artistas,
            "Popularidad Media (Artistas)": round(pop_media_artistas, 2),
            "Generos Promedio (Por Artista)": round(num_medio_generos_artistas, 2),
            "Seguidores Medios (Artistas)": round(seg_medios_artistas, 2),
            "Canciones Promedio (Playlists)": round(num_medio_canciones_pl, 2),
            "Seguidores Medios (Playlists)": round(seg_medios_pl, 2)
        }
        
        return vector_final, metricas_resumen