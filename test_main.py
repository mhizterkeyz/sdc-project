'''
Tests for jwt flask app.
'''
from email import header
import os
import json
import pytest

import main

SECRET = 'TestSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjY0MDQ5MjEsIm5iZiI6MTY2NTE5NTMyMSwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.QzKXsnnc5JPPawdWUAr3LDLggfgNMEwoD4LmiCNoV68'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

def test_content(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')
    token = response.json['token']
    response = client.get('/contents',
                           headers={'Authorization': f'Bearer {token}'},)

    assert response.status_code == 200
    email = response.json['email']
    exp = response.json['exp']
    nbf = response.json['nbf']
    assert email is not None
    assert exp is not None
    assert nbf is not None
