import json
import requests

def open_json():
	url = "https://epic.gsfc.nasa.gov/api/natural"
	response = requests.get(url).json()
	return response

def get_picture(response):
	most_recent_img = response[-1]
	date = most_recent_img['date']
	year = date[0:4]
	month = date[5:7]
	day = date[8:10]
	image_name = most_recent_img['image']
	pic_url = 'https://epic.gsfc.nasa.gov/archive/natural/' + year + '/' + month + '/' + day + '/jpg/' + image_name + '.jpg'
	pic_data = requests.get(pic_url).content

	with open('static/images/epic.jpg', 'wb') as pic:
		pic.write(pic_data)

	caption = [most_recent_img['caption'], most_recent_img['centroid_coordinates']['lat'], most_recent_img['centroid_coordinates']['lon'], year, month, day]

	return caption

def convert_month(month):

	if month == "01" or month == "1":
		date = "January"

	elif month == "02" or month == "2":
		date = "February"

	elif month == "03" or month == "3":
		date = "March"

	elif month == "04" or month == "4":
		date = "April"

	elif month == "05" or month == "5":
		date = "May"

	elif month == "06" or month == "6":
		date = "June"

	elif month == "07" or month == "7":
		date = "July"

	elif month == "08" or month == "8":
		date = "August"

	elif month == "09" or month == "9":
		date = "September"

	elif month == "10":
		date = "October"
	
	elif month == "11":
		date = "November"

	elif month == "12":
		date = "December"

	return date