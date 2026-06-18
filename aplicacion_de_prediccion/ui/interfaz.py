import gradio as gr
import datetime
from modelos.artista import Artista
from modelos.playlist import Playlist
from modelos.cancion import Cancion
from servicios.creador_de_features import CreadorDeFeatures
from servicios.predictor import Predictor

"""Siendo sincero, la interfaz la saque de un repositorio que me encontre por ahi,
solamente la modifique y adapte pq es la primera vez que trabajo con gradio lol """

creador_features = CreadorDeFeatures()
predictor = Predictor()

MAX_ITEMS = 5

def orquestar_prediccion(
    c_name, c_playable, c_album, c_date,
    cant_artistas, cant_playlists,
    *dinamicos
):
    try:
        # Validacion estricta de la fecha de lanzamiento 
        if c_date and str(c_date).strip():
            try:
                datetime.datetime.strptime(str(c_date).strip(), "%Y-%m-%d")
            except ValueError:
                return "Error: La fecha de lanzamiento debe tener el formato estricto YYYY-MM-DD.", ""

        # Los argumentos dinamicos vienen empaquetados. Los separamos
        offset_artistas = MAX_ITEMS * 4
        datos_artistas = dinamicos[:offset_artistas]
        datos_playlists = dinamicos[offset_artistas:]
        
        artistas_obj = []
        # Procesamos y validamos solo la cantidad de artistas actualmente visibles
        for i in range(int(cant_artistas)):
            uri = datos_artistas[i*4]
            pop = datos_artistas[i*4 + 1]
            gen = datos_artistas[i*4 + 2]
            fol = datos_artistas[i*4 + 3]
            
            # Validaciones numericas para Artista
            if pop is None:
                return f"Error: La popularidad del artista {i+1} es obligatoria.", ""
            if pop < 0 or pop > 100:
                return f"Error: La popularidad del artista {i+1} debe estar estrictamente entre 0 y 100.", ""
                
            if fol is None:
                return f"Error: Los seguidores del artista {i+1} son obligatorios.", ""
            if fol < 0:
                return f"Error: Los seguidores del artista {i+1} no pueden ser negativos.", ""
            
            artistas_obj.append(Artista(
                artist_popularity=pop, artist_genres=gen, artist_followers=fol, artist_uri=uri
            ))
                
        playlists_obj = []
        # Procesamos y validamos solo la cantidad de playlists actualmente visibles
        for i in range(int(cant_playlists)):
            uri = datos_playlists[i*7]
            name = datos_playlists[i*7 + 1]
            desc = datos_playlists[i*7 + 2]
            query = datos_playlists[i*7 + 3]
            auth = datos_playlists[i*7 + 4]
            n_tracks = datos_playlists[i*7 + 5]
            fol = datos_playlists[i*7 + 6]
            
            # Validaciones para Playlist
            if not name or str(name).strip() == "":
                return f"Error: El nombre de la playlist {i+1} es obligatorio.", ""
                
            if n_tracks is None:
                return f"Error: El numero de canciones de la playlist {i+1} es obligatorio.", ""
            if n_tracks < 1:
                return f"Error: La playlist {i+1} debe tener al menos 1 cancion.", ""
                
            if fol is None:
                return f"Error: Los seguidores de la playlist {i+1} son obligatorios.", ""
            if fol < 0:
                return f"Error: Los seguidores de la playlist {i+1} no pueden ser negativos.", ""
            
            playlists_obj.append(Playlist(
                name=name, n_tracks=n_tracks, playlist_followers=fol,
                uri=uri, description=desc, query=query, author=auth
            ))
                
        # Validar minimos del dominio
        if not artistas_obj:
            return "Error: Debes registrar al menos un artista valido.", ""
        if not playlists_obj:
            return "Error: Debes registrar al menos una playlist valida.", ""
            
        # 1. Construir Objeto Cancion
        cancion = Cancion(
            name=c_name, is_playable=c_playable, 
            artists=artistas_obj, playlists=playlists_obj,
            album_type=c_album, release_date=c_date
        )
        
        # 2. Obtener variables derivadas
        vector, metricas = creador_features.procesar(cancion)
        
        # 3. Ejecutar prediccion del modelo
        resultado = predictor.predecir(vector)
        
        # 4. Evaluacion binaria de la salida del algoritmo
        if int(round(resultado)) == 1:
            str_prediccion = "Exito"
        elif int(round(resultado)) == 0:
            str_prediccion = "Fracaso"
        else:
            str_prediccion = f"Resultado inesperado: {resultado}"
        
        # Formatear el resumen de metricas
        str_metricas = "\n".join([f"- {k}: {v}" for k, v in metricas.items()])
        
        return str_prediccion, str_metricas
        
    except Exception as e:
        return f"Ocurrio un error interno: {str(e)}", "Revisa los datos ingresados."


def revelar_siguiente(contador):
    """Aumenta el contador de elementos visibles sin superar el maximo."""
    if contador >= MAX_ITEMS:
        return [contador] + [gr.update() for _ in range(MAX_ITEMS)]
    nuevo_estado = contador + 1
    visibilidades = [gr.update(visible=(i < nuevo_estado)) for i in range(MAX_ITEMS)]
    return [nuevo_estado] + visibilidades


def ocultar_ultimo(contador):
    """Disminuye el contador de elementos visibles sin bajar de 1."""
    if contador <= 1:
        return [contador] + [gr.update() for _ in range(MAX_ITEMS)]
    nuevo_estado = contador - 1
    visibilidades = [gr.update(visible=(i < nuevo_estado)) for i in range(MAX_ITEMS)]
    return [nuevo_estado] + visibilidades


def crear_interfaz():
    tema = gr.themes.Monochrome(
        primary_hue="zinc",
        secondary_hue="neutral",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"]
    )
    
    with gr.Blocks(theme=tema, title="Predictor de exitos") as app:
        gr.Markdown(
            """
            # Predictor de Popularidad Musical
            Ingrese los datos de la cancion, sus artistas y las playlists en las que aparece para predecir si sera un exito o un fracaso.
            """
        )
        
        with gr.Row():
            # COLUMNA IZQUIERDA: Formularios y entradas de datos
            with gr.Column(scale=2):
                with gr.Accordion("Informacion de la Cancion", open=True):
                    c_name = gr.Textbox(label="Nombre de la cancion")
                    with gr.Row():
                        c_playable = gr.Checkbox(label="Es reproducible (is_playable)", value=True)
                        c_album = gr.Textbox(label="Tipo de Album  (single, album, compilation)")
                        c_date = gr.Textbox(label="Fecha de lanzamiento (YYYY-MM-DD)")
                
                # --- SECCION ARTISTAS ---
                gr.Markdown("### Artistas")
                estado_artistas = gr.State(1)
                bloques_artistas = []
                inputs_artistas = []
                
                for i in range(MAX_ITEMS):
                    with gr.Group(visible=(i == 0)) as bloque:
                        gr.Markdown(f"**Artista {i+1}**")
                        with gr.Row():
                            a_uri = gr.Textbox(label="URI (Opcional)")
                            a_pop = gr.Number(label="Popularidad (0-100)")
                        with gr.Row():
                            a_gen = gr.Textbox(label="Generos (separados por coma)", placeholder="pop, rock, indie")
                            a_fol = gr.Number(label="Seguidores")
                        
                        inputs_artistas.extend([a_uri, a_pop, a_gen, a_fol])
                        bloques_artistas.append(bloque)
                
                with gr.Row():
                    btn_add_artista = gr.Button("Agregar otro artista", size="sm")
                    btn_remove_artista = gr.Button("Eliminar ultimo artista", size="sm")
                    
                btn_add_artista.click(
                    revelar_siguiente, 
                    inputs=[estado_artistas], 
                    outputs=[estado_artistas] + bloques_artistas
                )
                btn_remove_artista.click(
                    ocultar_ultimo,
                    inputs=[estado_artistas],
                    outputs=[estado_artistas] + bloques_artistas
                )

                # --- SECCION PLAYLISTS ---
                gr.Markdown("### Playlists")
                estado_playlists = gr.State(1)
                bloques_playlists = []
                inputs_playlists = []
                
                for i in range(MAX_ITEMS):
                    with gr.Group(visible=(i == 0)) as bloque:
                        gr.Markdown(f"**Playlist {i+1}**")
                        with gr.Row():
                            p_uri = gr.Textbox(label="URI (Opcional)")
                            p_name = gr.Textbox(label="Nombre")
                        with gr.Row():
                            p_n_tracks = gr.Number(label="Numero de canciones")
                            p_fol = gr.Number(label="Seguidores de la playlist")
                        with gr.Accordion("Detalles Adicionales", open=False):
                            p_desc = gr.Textbox(label="Descripcion")
                            p_query = gr.Textbox(label="Query")
                            p_auth = gr.Textbox(label="Autor")
                            
                        inputs_playlists.extend([p_uri, p_name, p_desc, p_query, p_auth, p_n_tracks, p_fol])
                        bloques_playlists.append(bloque)
                
                with gr.Row():
                    btn_add_pl = gr.Button("Agregar otra playlist", size="sm")
                    btn_remove_pl = gr.Button("Eliminar ultima playlist", size="sm")
                    
                btn_add_pl.click(
                    revelar_siguiente, 
                    inputs=[estado_playlists], 
                    outputs=[estado_playlists] + bloques_playlists
                )
                btn_remove_pl.click(
                    ocultar_ultimo,
                    inputs=[estado_playlists],
                    outputs=[estado_playlists] + bloques_playlists
                )
                
                with gr.Row():
                    btn_predecir = gr.Button("Predecir Popularidad", variant="primary", size="lg")
                    btn_limpiar = gr.Button("Limpiar todos los datos", variant="secondary", size="lg")

            # COLUMNA DERECHA: Bloque de respuestas y salida del sistema
            with gr.Column(scale=1):
                gr.Markdown("### Resultados")
                out_prediccion = gr.Textbox(label="Prediccion Final", text_align="center")
                out_metricas = gr.Textbox(label="Resumen de Metricas Calculadas", lines=8)
                
        # Vinculacion del proceso de calculo y ejecucion de inferencia
        todas_las_entradas = [
            c_name, c_playable, c_album, c_date, 
            estado_artistas, estado_playlists
        ] + inputs_artistas + inputs_playlists
        
        btn_predecir.click(
            orquestar_prediccion,
            inputs=todas_las_entradas,
            outputs=[out_prediccion, out_metricas]
        )
        
        # Logica estructurada para restablecer el estado inicial de todos los componentes
        def ejecutar_limpieza():
            # Orden de retorno: c_name, c_playable, c_album, c_date, estado_artistas, estado_playlists, out_prediccion, out_metricas
            valores_base = ["", True, "", "", 1, 1, "", ""]
            
            # Limpieza de inputs correspondientes a los 5 artistas
            for _ in range(MAX_ITEMS):
                valores_base.extend(["", None, "", None])
                
            # Limpieza de inputs correspondientes a las 5 playlists
            for _ in range(MAX_ITEMS):
                valores_base.extend(["", "", "", "", "", None, None])
                
            # Forzar visibilidad inicial de los bloques (solo el primero activo)
            valores_base.append(gr.update(visible=True))
            for _ in range(MAX_ITEMS - 1):
                valores_base.append(gr.update(visible=False))
                
            valores_base.append(gr.update(visible=True))
            for _ in range(MAX_ITEMS - 1):
                valores_base.append(gr.update(visible=False))
                
            return valores_base

        todos_los_controles_interfaz = [
            c_name, c_playable, c_album, c_date, 
            estado_artistas, estado_playlists, 
            out_prediccion, out_metricas
        ] + inputs_artistas + inputs_playlists + bloques_artistas + bloques_playlists

        btn_limpiar.click(
            ejecutar_limpieza,
            inputs=[],
            outputs=todos_los_controles_interfaz
        )

    return app