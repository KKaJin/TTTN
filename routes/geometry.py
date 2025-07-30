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

@bp.route('/api/geometry/info')
def get_location_info():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)

    if lat is None or lng is None:
        return jsonify({'error': 'Thiếu toạ độ'}), 400

    point = Point(lng, lat)

    # Đọc dữ liệu
    provinces = read_geojson_folder(PROVINCE_DIR)
    communes = read_geojson_folder(COMMUNE_DIR)

    found_province = None
    found_commune = None
    communes_in_province = []

    # Tìm tỉnh chứa point
    for p in provinces:
        polygon = shape(p['geometry'])
        if polygon.contains(point):
            found_province = p
            break

    if found_province:
        # Tìm tất cả xã thuộc tỉnh đó
        ma_tinh = found_province['properties'].get('maTinh')
        for c in communes:
            if c['properties'].get('maTinh') == ma_tinh:
                communes_in_province.append(c)
                polygon = shape(c['geometry'])
                if polygon.contains(point):
                    found_commune = c

    return jsonify({
        'province': found_province,
        'commune': found_commune,
        'communes': communes_in_province
    })