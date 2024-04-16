import pytest
import pymongo
import os

@pytest.fixture(scope="session")
def mongodb():
    client = pymongo.MongoClient('mongodb://mongo:27017')
    assert client.admin.command("ping")["ok"] != 0.0
    return client