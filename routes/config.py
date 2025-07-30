import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROVINCE_DIR = os.path.join(BASE_DIR, 'data', 'geojson', 'provinces')
COMMUNE_DIR = os.path.join(BASE_DIR, 'data', 'geojson', 'communes')

ORS_KEY = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjcyMmFlZmJkOGJkYzRiMjA4OTYwMmNjNjg2NjZjZjJjIiwiaCI6Im11cm11cjY0In0='
ORS_URL = 'https://api.openrouteservice.org/v2/directions/driving-car'
