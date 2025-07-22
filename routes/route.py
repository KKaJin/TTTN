from flask import Blueprint, request
from config import ORS_KEY, ORS_URL
import requests

bp = Blueprint('route', __name__)

@bp.route('/api/route', methods=['POST'])
def get_route():
    data = request.get_json()
    headers = {
        'Authorization': ORS_KEY,
        'Content-Type': 'application/json'
    }
    body = {'coordinates': [data['start'], data['end']]}
    r = requests.post(ORS_URL, headers=headers, json=body)
    return r.json(), r.status_code
