from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
	return 'Hello World, I\'m {}'.format(name)

@app.route('/update_location', methods = ['Post'])
def update_location():
    json = request.get_json()	
    try: 
    	db_update_location(json)
    except KeyError:
    	return jsonify({"status":"error", "error":"missing args"}), 400
    except ValidationError as e:
    	return jsonify({"staus":"error", "error":e.description}), 400

    message = "location {} updated to coordinates {} {} ".format(json["address"], json["lat"], json["lon"])
    
    return jsonify({"status":"success", "message": message})

@app.route('/get_balance', methods = ['POST'])
def get_balance():
	json = request.get_json()
	try:
		balance = lookup_balance(json['account_number'], json['pin'])
	except KeyError:
		return jsonify({"status":"error", "message":"missing args"}), 400
	except ValidationError as e:
		return jsonify({"status":e.description}), 400
	return jsonify({"status":"success", "balance":balance})

def lookup_balance(account_number, pin):
	if account_number != "1111":
		raise ValidationError("account not found")
	elif pin != "0000":
		raise ValidationError("invalid pin")

	return 1000

def db_update_location(json):
	if "lat" not in json:
		raise ValidationError("lat not provided")
	elif "lon" not in json:
		raise ValidationError("lon not provided")
	elif not (type(json["lat"]) is float or type(json["lat"]) is int):
		raise ValidationError("lat must be float or int value")
	elif not (type(json["lon"]) is float or type(json["lon"]) is int):
		raise ValidationError("lon must be a float or an int value")
	elif not 90 > json["lat"] > -90:
		raise ValidationError("lat must be a number between -90 and 90")
	elif not 180 > json["lon"] > -180:
		raise ValidationError("lon must be a number between -180 and 180")
	else:
		pass



class ValidationError(Exception):
	def __init__(self, description):
		self.description = description


if __name__ == '__main__':
	app.run(debug = True)