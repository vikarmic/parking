import sqlalchemy
from flask import Flask, request
import json
from geopy.distance import vincenty

from db import ParkingSpot, Session

app = Flask('api')

def direct_get_slot(request_json, session):
	ret = None
	if 'id' in request_json:
		ret = session.query(ParkingSpot).filter_by(id=request_json['id']).one_or_none()
	elif 'latitude' in request_json and 'longitude' in request_json:
		ret = session.query(ParkingSpot).filter_by(latitude=request_json['latitude']).filter_by(longitude=request_json['longitude']).one_or_none()
	session.close()
	return ret

def check_phone(phone_string):
	clean_phone_string = phone_string.replace('-', '')
	try:
		int(clean_phone_string)
		return True
	except ValueError:
		return False

def dist_within_radius(slot, lat, lon, radius):
	point1 = (slot.latitude, slot.longitude)
	point2 = (lat, lon)
	return (vincenty(point1, point2).miles <= radius)

@app.route('/parking/available', methods=['GET'])
def get_available_slots():
	session = Session()
	slots = session.query(ParkingSpot).filter(ParkingSpot.reserved==False).all()
	return json.dumps([s.as_dict() for s in slots])

@app.route('/parking/available', methods=['POST'])
def get_available_slots_near():
	session = Session()
	request_data = request.get_json()
	lat = request_data['latitude']
	lon = request_data['longitude']
	rad = request_data['radius']
	slots = session.query(ParkingSpot).filter(ParkingSpot.reserved==False).all()
	return json.dumps([s.as_dict() for s in slots if dist_within_radius(s, lat, lon, rad)])

@app.route('/parking/reserve', methods=['GET'])
def get_reservations():
	session = Session()
	slots = session.query(ParkingSpot).filter(ParkingSpot.reserved==True).all()
	return json.dumps([s.as_dict() for s in slots])

@app.route('/parking/reserve', methods=['POST'])
def reserve_slot():
	request_data = request.get_json()
	if 'phone' not in request_data:
		return json.dumps({'error': 'User must provide a phone number'}), 400
	if not check_phone(request_data['phone']):
		return json.dumps({'error': 'User phone number is not valid'}), 400
	session = Session()
	slot = direct_get_slot(request_data, session)
	if slot is None:
		return json.dumps({'error': 'Specified parking slot does not exist'}), 404
	if slot.reserved:
		return json.dumps({'error': 'Specified parking slot already reserved'}), 400
	slot.reserved = True
	slot.user_phone = request_data['phone']
	session.add(slot)
	session.commit()
	ret = "Slot reserved: " + str(slot.id)
	session.close()
	return ret


@app.route('/parking/reserve', methods=['DELETE'])
def cancel_reservation():
	request_data = request.get_json()
	if 'phone' not in request_data:
		return json.dumps({'error': 'User must provide a phone number'}), 400
	session = Session()
	slot = direct_get_slot(request_data, session)
	if slot is None:
		return json.dumps({'error': 'Specified parking slot does not exist'}), 404
	if slot.user_phone != request_data['phone']:
		return json.dumps({'error': 'User phone number does not match phone of record'}), 400
	slot.reserved = False
	slot.user_phone = None
	session.add(slot)
	session.commit()
	ret = "Reservation cancelled on slot " + str(slot.id)
	session.close()
	return ret

@app.route('/parking/cost', methods=['POST'])
def show_cost():
	request_data = request.get_json()
	session = Session()
	slot = direct_get_slot(request_data, session)
	if slot is None:
		return json.dumps({'error': 'Specified parking slot does not exist'}), 404
	return json.dumps({'cost': '$%.2f' % slot.price})


if __name__ == '__main__':
    app.run()
	