from flask import Flask, render_template, request
from hazards import is_hazardous
from epic import open_json, get_picture, convert_month
import json
import datetime
import requests

application = app = Flask(__name__)

@app.route('/')
def index():
	names = []
	date = []
	form_hazard_data = []


	date = datetime.datetime.now()
	url_date = date.strftime('%Y-%m-%d')
	url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={url_date}&api_key=r1iHbGrK7QNYLHoWQOE7733aQzZCBGGCoFTKr656"
	python_dict = requests.get(url).json()

	date = []
	dates = []
	root = python_dict['near_earth_objects']
	for date in root:
		dates.append(date)

	num = 0
	data_list = []
	for date in dates:
		for obj in python_dict['near_earth_objects'][date]:
			if num < len(python_dict['near_earth_objects'][date]):
				name = python_dict['near_earth_objects'][date][num]['name']
				diameter_min = python_dict['near_earth_objects'][date][num]['estimated_diameter']['miles']['estimated_diameter_min']
				diameter_max = python_dict['near_earth_objects'][date][num]['estimated_diameter']['miles']['estimated_diameter_max']
				hazardous = python_dict['near_earth_objects'][date][num]['is_potentially_hazardous_asteroid']
				miss_distance = python_dict['near_earth_objects'][date][num]['close_approach_data'][0]['miss_distance']['miles']
				velocity = python_dict['near_earth_objects'][date][num]['close_approach_data'][0]['relative_velocity']['miles_per_hour']
				date_full = python_dict['near_earth_objects'][date][num]['close_approach_data'][0]['close_approach_date_full']
				data = [ miss_distance, name, diameter_min, diameter_max, hazardous, velocity, date_full]
				data_list.append(data)
				num += 1
			else:
				num = 0
				data = None

	hazard_data = is_hazardous(data_list)
	for i in hazard_data:
		i[5] = float(i[5])
	for i in hazard_data:
		i[0] = float(i[0])
	for i in hazard_data:
		if i[1] not in form_hazard_data:
			form_hazard_data.append(i)
	form_hazard_data.sort()

	closest = form_hazard_data[0]
	return render_template('index.html', closest=closest)

@app.route('/epic')
def epic():
	response = open_json()
	caption = get_picture(response)
	text = caption[0]
	lat = caption[1]
	lon = caption[2]
	year = caption[3]
	month = convert_month(caption[4])
	day = caption[5]
	return render_template('epic.html', text=text, lat=lat, lon=lon, year=year, month=month, day=day)

@app.route('/hazard-list')
def hazard_list():
	form_hazard_data = []

	date = datetime.datetime.now()
	url_date = date.strftime('%Y-%m-%d')
	url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={url_date}&api_key=r1iHbGrK7QNYLHoWQOE7733aQzZCBGGCoFTKr656"
	python_dict = requests.get(url).json()

	date = []
	dates = []
	root = python_dict['near_earth_objects']
	for date in root:
		dates.append(date)

	num = 0
	data_list = []
	for date in dates:
		for obj in python_dict['near_earth_objects'][date]:
			if num < len(python_dict['near_earth_objects'][date]):
				name = python_dict['near_earth_objects'][date][num]['name']
				diameter_min = python_dict['near_earth_objects'][date][num]['estimated_diameter']['miles']['estimated_diameter_min']
				diameter_max = python_dict['near_earth_objects'][date][num]['estimated_diameter']['miles']['estimated_diameter_max']
				hazardous = python_dict['near_earth_objects'][date][num]['is_potentially_hazardous_asteroid']
				miss_distance = python_dict['near_earth_objects'][date][num]['close_approach_data'][0]['miss_distance']['miles']
				velocity = python_dict['near_earth_objects'][date][num]['close_approach_data'][0]['relative_velocity']['miles_per_hour']
				date_full = python_dict['near_earth_objects'][date][num]['close_approach_data'][0]['close_approach_date_full']
				data = [ miss_distance, name, diameter_min, diameter_max, hazardous, velocity, date_full]
				data_list.append(data)
				num += 1
			else:
				num = 0
				data = None



	hazard_data = is_hazardous(data_list)
	for i in hazard_data:
		i[5] = float(i[5])
	for i in hazard_data:
		i[0] = float(i[0])
	for i in hazard_data:
		if i[1] not in form_hazard_data:
			form_hazard_data.append(i)
	form_hazard_data.sort()

	return render_template('hazard_list.html', form_hazard_data=form_hazard_data)