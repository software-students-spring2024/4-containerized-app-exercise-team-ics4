import pytest
from flask import Flask
from mongomock import MongoClient
from unittest.mock import patch

from app import app as flask_app

@pytest.fixture(scope='module')
def app():
    # use mongo mock to isolate testing from prod db
    with patch('pymongo.MongoClient', MongoClient):
        db = MongoClient().audio_feed
        collection = db.status
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

        flask_app.config.update({
            "TESTING": True,
            "MONGO_URI": "mongomock://localhost"
        })

        yield flask_app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()