from flask import Blueprint, request, jsonify
import os, json
from config import PROVINCE_DIR, COMMUNE_DIR

bp = Blueprint('info', __name__)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@bp.route('/api/geometry/provinces')
def get_all_provinces():
    provinces_data = []
    for filename in os.listdir(PROVINCE_DIR):
        if filename.endswith(".geojson"):
            data = read_file(os.path.join(PROVINCE_DIR, filename))
            for feature in data['features']:
                props = feature.get('properties', {})
                provinces_data.append({
                    "maTinh_BNV": props.get("maTinh_BNV"),
                    "tenTinh": props.get("tenTinh"),
                    "dienTich": props.get("dienTich"),
                    "danSo": props.get("danSo"),
                })
    return jsonify({
        "count": len(provinces_data),
        "provinces": provinces_data
    })


@bp.route('/api/geometry/communes/<province_name>')
def get_communes_by_province(province_name):
    commune_file = os.path.join(COMMUNE_DIR, f"{province_name}.geojson")
    data = read_file(commune_file)
    communes_data = []
    for feature in data['features']:
        props = feature.get('properties', {})
        communes_data.append({
            "tenTinh": props.get("tenTinh"),
            "maTinh_BNV": props.get("maTinh_BNV"),
            "tenXa": props.get("tenXa"),
            "maXa": props.get("maXa"),
            "maXa_BNV": props.get("maXa_BNV"),
            "danSo": props.get("danSo"),
            "dienTich": props.get("dienTich"),
        })

    return jsonify({
        "province": province_name,
        "count": len(communes_data),
        "communes": communes_data
    })

