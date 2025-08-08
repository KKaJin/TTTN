from flask import Blueprint, request, jsonify
import json
import os

bp = Blueprint('search', __name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PROVINCES_FILE = os.path.join(DATA_DIR, 'DiaPhan_Tinh_2025.geojson.geojson')
COMMUNES_FILE = os.path.join(DATA_DIR, 'DiaPhan_Xa_2025.geojson')

@bp.route('/api/search')
def search():
    query = request.args.get('q', '').strip().lower()

    results = []
    with open(PROVINCES_FILE, 'r', encoding='utf-8') as f:
        provinces = json.load(f)

    for feature in provinces['features']:
        ten_tinh = feature['properties'].get('tenTinh', '').lower()
        if query in ten_tinh:
            results.append({
                'type': 'province',
                'maTinh_BNV': feature['properties'].get('maTinh_BNV'),
                'tenTinh': feature['properties'].get('tenTinh'),
                'dienTich': feature['properties'].get('dienTich'),
                'danSo': feature['properties'].get('danSo')
            })

    with open(COMMUNES_FILE, 'r', encoding='utf-8') as f:
        communes = json.load(f)

    for feature in communes['features']:
        ten_xa = feature['properties'].get('tenXa', '').lower()
        ten_tinh = feature['properties'].get('tenTinh', '').lower()
        if query in ten_xa or query in ten_tinh:
            results.append({
                'type': 'commune',
                'tenTinh': feature['properties'].get('tenTinh'),
                'maTinh_BNV': feature['properties'].get('maTinh_BNV'),
                'tenXa': feature['properties'].get('tenXa'),
                'maXa': feature['properties'].get('maXa'),
                'maXa_BNV': feature['properties'].get('maXa_BNV'),
                'danSo': feature['properties'].get('danSo'),
                'dienTich': feature['properties'].get('dienTich')
            })

    return jsonify(results)
