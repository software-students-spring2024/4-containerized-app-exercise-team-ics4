from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("localhost", 27017)
db = client.camera_live_feed
status_collection = db.status

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/status', methods=['GET'])
def get_status():
    status = status_collection.find_one({})

    # Convert MongoDB document to JSON
    if status:
        obj = {
            "loading": status.get("loading"),
            "gesture": status.get("gesture"),
            "confidence": status.get("confidence"),
            "cameraConnected": status.get("cameraConnected")
        }
    else:
        obj = {"error": "error"}

    # Send JSON response to frontend
    return jsonify(obj)


@app.route('/reset_status', methods=['POST'])
def reset_status():
    try:
        initial_status = {
			"loading": True,
			"gesture": "",
			"confidence": 0
		}
        status_collection.update_one({}, {"$set": initial_status})
        return jsonify({"success": True, "message": "Status reset to initial state"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)