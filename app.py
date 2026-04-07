from flask import Flask, request, render_template_string
import yt_dlp
import socket
import os

app = Flask(__name__)

# Lista en memoria para los videos destacados (simulación de base de datos)
videos_destacados = []

# Interfaz HTML con estilo tipo Instagram
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>InstaDownloader - Lab 04</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fafafa; display: flex; justify-content: center; padding-top: 50px; }
        .card { background: white; border: 1px solid #dbdbdb; padding: 30px; border-radius: 8px; width: 400px; text-align: center; }
        h2 { color: #262626; margin-bottom: 20px; }
        input { width: 90%; padding: 10px; margin-bottom: 10px; border: 1px solid #efefef; border-radius: 3px; background: #fafafa; }
        .btn-download { background-color: #0095f6; color: white; border: none; padding: 10px; width: 95%; border-radius: 4px; font-weight: bold; cursor: pointer; }
        .btn-show { background-color: #262626; color: white; border: none; padding: 10px; width: 95%; border-radius: 4px; margin-top: 10px; cursor: pointer; }
        .list-container { margin-top: 20px; text-align: left; border-top: 1px solid #efefef; padding-top: 15px; }
        .video-item { font-size: 14px; color: #262626; padding: 5px 0; border-bottom: 1px solid #fafafa; }
        .hostname { font-size: 12px; color: #8e8e8e; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📸 InstaDownloader</h2>
        
        <form method="POST" action="/analizar">
            <input type="text" name="url" placeholder="Pega el link de Instagram aquí..." required>
            <button type="submit" class="btn-download">Descargar / Analizar</button>
        </form>

        <form method="GET" action="/">
            <button type="submit" name="ver" value="1" class="btn-show">Mostrar Videos Destacados</button>
        </form>

        {% if lista_videos %}
        <div class="list-container">
            <strong>🌟 Videos Destacados:</strong>
            {% for video in lista_videos %}
                <div class="video-item">📌 {{ video }}</div>
            {% endfor %}
        </div>
        {% endif %}

        <div class="hostname">Contenedor: {{ hostname }}</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ver_lista = request.args.get('ver') == '1'
    return render_template_string(HTML_UI, 
                                 hostname=socket.gethostname(), 
                                 lista_videos=videos_destacados if ver_lista else None)

@app.route('/analizar', methods=['POST'])
def analizar():
    url = request.form.get('url')
    try:
        # Extraemos información del video
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            titulo = info.get('title', 'Video de Instagram')
            # Lo agregamos a destacados
            if titulo not in videos_destacados:
                videos_destacados.append(titulo)
        return f"<h1>Video '{titulo}' analizado con éxito.</h1><a href='/?ver=1'>Volver y ver lista</a>"
    except Exception as e:
        return f"<h1>Error: Enlace no válido</h1><a href='/'>Volver</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)