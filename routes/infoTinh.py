from flask import Blueprint, jsonify
import os, json

bp = Blueprint('infoprovince', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'DiaPhan_Tinh_2025.geojson')

# Lấy hết thông tin trong file tỉnh
@bp.route('/api/infoprovince/provinces', methods=['GET'])
def get_province_all():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# Lấy thông tin 1 tỉnh trong file
@bp.route('/api/infoprovince/<maTinh_BNV>', methods=['GET'])
def get_province_info_1(maTinh_BNV):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    features = [f for f in data['features'] 
                if f['properties'].get('maTinh_BNV') == maTinh_BNV and 'tenXa' not in f['properties']]
    return jsonify({"type": "FeatureCollection", "features": features})

# Lấy thông tin 1 tỉnh trong file nhưng chỉ lấy thông tin cần thiết
@bp.route('/api/infoprovince/<maTinh_BNV>', methods=['GET'])
def get_province_info_1f(maTinh_BNV):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    infoTinh = []
    for feat in data['features']:
        p = feat['properties']
        if p.get('maTinh_BNV') == maTinh_BNV and 'tenXa' not in p:
            infoTinh.append({
                "maTinh_BNV": p.get("maTinh_BNV"),
                "tenTinh": p.get("tenTinh"),
                "dienTich": p.get("dienTich"),
                "danSo": p.get("danSo")
            })
    return jsonify(infoTinh)
