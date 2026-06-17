from ui.interfaz import crear_interfaz

if __name__ == "__main__":
    print("Iniciando la aplicación...")
    app = crear_interfaz()
    app.launch(server_name="localhost", server_port=7860)