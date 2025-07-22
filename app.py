from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from routes import geometry, route, search, markers

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '../frontend'),
    static_url_path=''
)
CORS(app)

app.register_blueprint(geometry.bp)
app.register_blueprint(route.bp)
app.register_blueprint(search.bp)
app.register_blueprint(markers.bp)
# url_prefix='/api'

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
