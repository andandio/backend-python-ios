from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/hello/<name>')

def hello(name):
	return 'Hello World, I\'m {}'.format(name)

@app.route('/update_location', methods = ['Post'])

def update_location():
    json = request.get_json()	
    error = update_location_validation_error(json)
    if error:
    	return jsonify({"status":error}), 400

    message = "location {} updated to coordinates {} {} ".format(json["address"], json["lat"], json["lon"])
    
    return jsonify({"status":"success", "message": message})

def update_location_validation_error(json):
	if "lat" not in json:
		return "lat not provided"
	if "lon" not in json:
		return "lon not provided"
	if not (type(json["lat"]) is float or type(json["lat"]) is int):
		return "lat must be float or int value"
	if not (type(json["lon"]) is float or type(json["lon"]) is int):
		return "lon must be a float or an int value"
	if not 90 > json["lat"] > -90:
		return "lat must be a number between -90 and 90"
	if not 180 > json["lon"] > -180:
		return "lon must be a number between -180 and 180"
	return None



if __name__ == '__main__':
	app.run(debug = True)