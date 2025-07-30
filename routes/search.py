from flask import Blueprint, request, jsonify
import requests

bp = Blueprint('search', __name__)

@bp.route('/api/search')
def search():
    query = request.args.get('query')
    url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5'
    headers = {'User-Agent': 'Ban do hanh chinh'}
    r = requests.get(url ,headers=headers) 
    data = r.json()

    results = [{
        'name': d['display_name'],
        'lat': float(d['lat']),
        'lng': float(d['lon']),
        'type': d.get('type'),
        'display_name': d.get('display_name')
    } for d in data]
    return jsonify(results)
