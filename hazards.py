

def is_hazardous(data_list):
	hazard_data = []
	for i in data_list:
		if i[4]  == True:
			hazard_data.append(i)
	return hazard_data