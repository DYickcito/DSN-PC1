python
from flask import Flask, request, render_template_string, send_from_directory
import yt_dlp
import socket
import os

app = Flask(__name__)

# Carpeta donde se guardarán los videos dentro del contenedor
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Lista de videos destacados (nombre del archivo y título)
videos_destacados = []

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>InstaDownloader Pro - Lab 04</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #fafafa; display: flex; justify-content: center; padding-top: 50px; }
        .card { background: white; border: 1px solid #dbdbdb; padding: 30px; border-radius: 8px; width: 450px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h2 { color: #262626; }
        input { width: 90%; padding: 10px; margin-bottom: 10px; border: 1px solid #efefef; border-radius: 3px; }
        .btn-download { background-color: #0095f6; color: white; border: none; padding: 12px; width: 95%; border-radius: 4px; font-weight: bold; cursor: pointer; }
        .btn-show { background-color: #262626; color: white; border: none; padding: 10px; width: 95%; border-radius: 4px; margin-top: 10px; cursor: pointer; }
        .list-container { margin-top: 20px; text-align: left; border-top: 1px solid #efefef; padding-top: 15px; }
        .video-item { font-size: 14px; padding: 10px; border-bottom: 1px solid #fafafa; display: flex; justify-content: space-between; align-items: center; }
        .download-link { color: #0095f6; text-decoration: none; font-weight: bold; font-size: 12px; border: 1px solid #0095f6; padding: 2px 8px; border-radius: 4px; }
        .hostname { font-size: 11px; color: #8e8e8e; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📸 InstaDownloader Nube</h2>
        <form method="POST" action="/procesar">
            <input type="text" name="url" placeholder="URL de Instagram o Youtube" required>
            <button type="submit" class="btn-download">🚀 Descargar ahora</button>
        </form>

        <form method="GET" action="/">
            <button type="submit" name="ver" value="1" class="btn-show">📋 Ver Videos Destacados</button>
        </form>

        {% if lista_videos %}
        <div class="list-container">
            <strong>🌟 Videos en el Servidor:</strong>
            {% for video in lista_videos %}
                <div class="video-item">
                    <span>🎬 {{ video.titulo[:30] }}...</span>
                    <a href="/ficheros/{{ video.archivo }}" class="download-link" download>Bajar a PC</a>
                </div>
            {% endfor %}
        </div>
        {% endif %}
        <div class="hostname">ID Contenedor: {{ hostname }}</div>
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

@app.route('/procesar', methods=['POST'])
def procesar():
    url = request.form.get('url')
    try:
        # Configuración para descargar el video real
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'best',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            nombre_archivo = os.path.basename(filename)
            titulo = info.get('title', 'Video')
            
            # Guardamos en la lista de destacados
            videos_destacados.append({'titulo': titulo, 'archivo': nombre_archivo})
            
        return f"<h1>¡Descarga completada en AWS!</h1><p>{titulo}</p><a href='/?ver=1'>Ir a la lista de destacados</a>"
    except Exception as e:
        return f"<h1>Error al descargar</h1><p>{str(e)}</p><a href='/'>Volver</a>"

# RUTA CLAVE: Permite descargar el archivo desde el contenedor a tu PC física
@app.route('/ficheros/<path:filename>')
def descargar_archivo(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)