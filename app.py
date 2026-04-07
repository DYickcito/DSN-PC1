from flask import Flask, request, render_template_string, send_from_directory
import yt_dlp
import os
import socket

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Lista en memoria para "videos destacados" (en un caso real sería una base de datos)
videos_descargados = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>InstaDownloader - Lab 04</title>
    <style>
        body { font-family: Arial; text-align: center; background: #fafafa; padding: 30px; }
        .card { background: white; padding: 20px; border-radius: 10px; shadow: 0 2px 5px rgba(0,0,0,0.1); display: inline-block; width: 400px; }
        input { width: 80%; padding: 10px; margin: 10px 0; border: 1px solid #dbdbdb; }
        .btn-download { background: #0095f6; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .btn-show { background: #262626; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        .video-list { text-align: left; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📸 InstaDownloader</h2>
        <p>Hostname: {{ hostname }}</p>
        <form method="POST" action="/descargar">
            <input type="text" name="url" placeholder="URL de Instagram" required>
            <br>
            <button type="submit" class="btn-download">Descargar Video</button>
        </form>
        
        <form method="GET" action="/">
            <button type="submit" name="show" value="true" class="btn-show">Mostrar Destacados</button>
        </form>

        {% if mostrar_lista %}
        <div class="video-list">
            <h4>Videos Destacados:</h4>
            <ul>
                {% for video in lista %}
                    <li>{{ video }}</li>
                {% else %}
                    <li>No hay videos aún.</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    mostrar = request.args.get('show') == 'true'
    return render_template_string(HTML_TEMPLATE, 
                                 hostname=socket.gethostname(), 
                                 lista=videos_descargados, 
                                 mostrar_lista=mostrar)

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get('url')
    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            videos_descargados.append(info.get('title', 'Video sin título'))
        return f"<h1>Éxito: {info.get('title')} descargado.</h1><a href='/'>Volver</a>"
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1><a href='/'>Volver</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)