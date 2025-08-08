from flask import Blueprint, jsonify
import os, json

bp = Blueprint('infocommune', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'DiaPhan_Xa_2025.geojson')

# Lấy hết thông tin trong file xã theo mã tỉnh
@bp.route('/api/infocommune/<maTinh_BNV>' , methods=['GET'])
def get_commune_all(maTinh_BNV):
    with open(DATA_FILE , 'r', encoding='utf-8') as f:
        data = json.load(f)
    features = [f for f in data['features'] 
                if f['properties'].get('maTinh_BNV') == maTinh_BNV and 'tenXa' in f['properties']]
    return jsonify({"type": "FeatureCollection", "features": features})

# Lấy thông tin các xã nhưng chỉ lấy thông tin cần thiết
@bp.route('/api/infocommune/<maTinh_BNV>', methods=['GET'])
def get_commune_info_f(maTinh_BNV):
    with open(DATA_FILE , 'r', encoding='utf-8') as f:
        data = json.load(f)
    infoXa = []
    for feat in data['features']:
        p = feat['properties']
        if p.get('maTinh_BNV') == maTinh_BNV and 'tenXa' in p:
            infoXa.append({
                "tenTinh": p.get("tenTinh"),
                "maTinh_BNV": p.get("maTinh_BNV"),
                "tenXa": p.get("tenXa"),
                "maXa": p.get("maXa"),
                "maXa_BNV": p.get("maXa_BNV"),
                "danSo": p.get("danSo"),
                "dienTich": p.get("dienTich")
            })
    return jsonify(infoXa)

# Lấy thông tin 1 xã nhưng chỉ lấy thông tin cần thiết
@bp.route('/api/infocommune/<maTinh_BNV>/<maXa_BNV>', methods=['GET'])
def get_commune_info_1f(maTinh_BNV, maXa_BNV):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for feature in data['features']:
        p = feature['properties']
        if p.get('maTinh_BNV') == maTinh_BNV and p.get('maXa_BNV') == maXa_BNV:
            return jsonify({
                "tenTinh": p.get("tenTinh"),
                "maTinh_BNV": p.get("maTinh_BNV"),
                "tenXa": p.get("tenXa"),
                "maXa_BNV": p.get("maXa_BNV"),
                "danSo": p.get("danSo"),
                "dienTich": p.get("dienTich")
            })



