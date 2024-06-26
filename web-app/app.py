"""Import modules"""

import os
from flask import Flask, render_template, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
db = client.audio_feed
status_collection = db.status


@app.route("/")
@app.route("/index")
def index():
    """returns iframe content"""
    frame_src = os.getenv("FRAME_SRC", "http://localhost:1000")
    return render_template("index.html", frame_src=frame_src)


@app.route("/status", methods=["GET"])
def get_status():
    """get status of mongodb from ml client"""
    status = status_collection.find_one({})

    # Convert MongoDB document to JSON
    if status:
        obj = {
            "loading": status.get("loading"),
            "sound1": status.get("sound1"),
            "confidence1": status.get("confidence1"),
            "sound2": status.get("sound2"),
            "confidence2": status.get("confidence2"),
            "sound3": status.get("sound3"),
            "confidence3": status.get("confidence3"),
            "microphoneConnected": status.get("microphoneConnected"),
        }
    else:
        obj = {"error": "error"}

    # Send JSON response to frontend
    return jsonify(obj)


@app.route("/reset_status", methods=["POST"])
def reset_status():
    """reset mongodb status to initial status"""
    try:
        initial_status = {
            "loading": True,
            "sound1": "",
            "confidence1": 0,
            "sound2": "",
            "confidence2": 0,
            "sound3": "",
            "confidence3": 0,
            "microphoneConnected": False,
        }
        status_collection.update_one({}, {"$set": initial_status})
        return jsonify({"success": True, "message": "Status reset to initial state"})
    except errors.ConnectionFailure:
        return (
            jsonify({"success": False, "error": "Failed to connect to MongoDB."}),
            503,
        )
    except errors.OperationFailure as e:
        return (
            jsonify({"success": False, "error": "MongoDB operation failed: " + str(e)}),
            500,
        )
    except errors.PyMongoError as e:
        return (
            jsonify({"success": False, "error": "Database error occurred: " + str(e)}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
