from flask import Flask, request, render_template_string, send_from_directory
import yt_dlp
import socket
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

videos_destacados = []

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>InstaDownloader - Lab 04</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fafafa; display: flex; justify-content: center; padding: 40px; }
        .container { background: white; border: 1px solid #dbdbdb; padding: 25px; border-radius: 10px; width: 400px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn { background: #0095f6; color: white; border: none; padding: 12px; width: 95%; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .item { font-size: 14px; padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        input { width: 90%; padding: 10px; border: 1px solid #dbdbdb; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🐳 InstaDownloader AWS</h2>
        <form method="POST" action="/descargar">
            <input type="text" name="url" placeholder="URL de Instagram aquí" required>
            <button type="submit" class="btn">🚀 Descargar</button>
        </form>
        <form action="/" method="GET">
            <button type="submit" name="ver" value="1" class="btn" style="background:#262626">📋 Ver Destacados</button>
        </form>
        {% if lista %}
        <div style="text-align:left; margin-top:20px;">
            <strong>Videos Destacados:</strong>
            {% for v in lista %}
            <div class="item">
                <span>🎬 {{ v.titulo[:20] }}...</span>
                <a href="/ficheros/{{ v.archivo }}" download style="color:#0095f6; text-decoration:none; font-weight:bold;">Bajar</a>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        <p style="font-size:10px; color:#999; margin-top:15px;">ID Host: {{ hostname }}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    ver = request.args.get('ver') == '1'
    return render_template_string(HTML_UI, hostname=socket.gethostname(), lista=videos_destacados if ver else None)

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get('url')
    try:
        ydl_opts = {'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            archivo = os.path.basename(ydl.prepare_filename(info))
            titulo = info.get('title', 'Video')
            videos_destacados.append({'titulo': titulo, 'archivo': archivo})
        return f"<h1>Éxito!</h1><p>{titulo}</p><a href='/?ver=1'>Volver a la lista</a>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p><a href='/'>Volver</a>"

@app.route('/ficheros/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)