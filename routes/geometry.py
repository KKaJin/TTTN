from flask import Blueprint, request, jsonify
import os, json
from config import PROVINCE_DIR, COMMUNE_DIR

bp = Blueprint('geometry', __name__)

def read_geojson_folder(folder):
    features = []
    for filename in os.listdir(folder):
        if filename.endswith('.geojson'):
            path = os.path.join(folder, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                features.extend(data.get('features', []))
    return {"type": "FeatureCollection", "features": features}

@bp.route('/api/geometry/all')
def get_all_geojson():
    try:
        provinces = read_geojson_folder(PROVINCE_DIR)
        communes = read_geojson_folder(COMMUNE_DIR)
        return jsonify({'province': provinces, 'commune': communes})
    except Exception as e:
        return jsonify({'error': str(e)})

@bp.route('/api/geometry/commune')
def get_commune_by_province():
    province_name = request.args.get('province')
    file_path = os.path.join(COMMUNE_DIR, f'{province_name}.geojson')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
