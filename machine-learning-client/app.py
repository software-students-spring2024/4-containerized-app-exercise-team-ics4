from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.audio_feed
collection = db.status

# initial object 
status_object = {
    "loading": True,
    "sound1": "",
    "confidence1": "",
    "sound2": "", 
    "confidence2": "",
    "sound3": "",
    "confidence3": "",
    "microphoneConnected": False
}
collection.delete_many({})
collection.insert_one(status_object)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route('/update', methods=['POST'])
def update_status():
    data = request.json

    result = collection.update_one(
        {}, 
        {'$set': {
			"loading": data.get('loading', False),
			"sound1": data.get('sound1', ''),
			"confidence1": data.get('confidence1', ''),
			"sound2": data.get('sound2', ''), 
			"confidence2": data.get('confidence2', ''),
			"sound3": data.get('sound3', ''),
			"confidence3": data.get('confidence3', ''),
			"microphoneConnected": data.get('microphoneConnected', False)
		}}
    )

    if result.modified_count > 0:
        return jsonify({"success": True, "message": "Status updated successfully"}), 200
    else:
        return jsonify({"success": False, "message": "No changes made"}), 200
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1000, debug=True)