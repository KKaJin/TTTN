# from flask import Blueprint, request, jsonify
# import requests

# bp = Blueprint('search', __name__)

# @bp.route('/api/search')
# def search():
#     query = request.args.get('query')
#     url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5'
#     headers = {'User-Agent': 'Ban do hanh chinh'}
#     r = requests.get(url ,headers=headers) 
#     data = r.json()

#     results = [{
#         'name': d['display_name'],
#         'lat': float(d['lat']),
#         'lng': float(d['lon']),
#         'type': d.get('type'),
#         'display_name': d.get('display_name')
#     } for d in data]
#     return jsonify(results)
from flask import Blueprint, request, jsonify
import requests

bp = Blueprint('search', __name__)

ARCGIS_URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
ARCGIS_API_KEY = "AAPTxy8BH1VEsoebNVZXo8HurNZG5ONfvDya2I1ZI_AuS8H0K8w1cQKF8abyBZph2b1NQT0J_Mz_2QS5-P_AF5IW1JiSHUS7lLqtWI1t0CI3dIjupm0Le6xbTm2Ys2Nv_oGXk06ODd-I7MKHX6QIt7RtEzPJvLF5cQ8pUcEk5Gh7LIOubTfcNZYy-Y7EjOl2amwUEQPPBP_1s2QZH0yZTbgyVFgJ1NdrCWItmcHWxCvwfRM.AT1_GpEB0eFK"  # API key từ ArcGIS Developer

@bp.route('/api/search')
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Thiếu tham số query'}), 400

    params = {
        "f": "json",
        "singleLine": query,
        "maxLocations": 5,
        "token": ARCGIS_API_KEY  # Truyền API key tại đây
    }

    r = requests.get(ARCGIS_URL, params=params)
    r.raise_for_status()
    data = r.json()

    if 'candidates' not in data:
        return jsonify([])

    results = [{
        'name': c.get('address'),
        'lat': c['location']['y'],
        'lng': c['location']['x'],
        'score': c.get('score', 0),
        'type': c.get('attributes', {}).get('Addr_type', 'unknown')
    } for c in data['candidates']]

    return jsonify(results)
