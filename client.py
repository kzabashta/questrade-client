#!/usr/bin/env python

import asyncio
import websockets
import requests

OAUTH_SERVICE_URL = 'https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token='

def __initialize_auth_request(refresh_token):
    r = requests.get(OAUTH_SERVICE_URL + refresh_token)
    return r.json()

def __get_access_token(auth_response):
    return auth_response['access_token']

def __get_api_uri(auth_response):
    print(auth_response)
    return auth_response['api_server']

def __build_auth_header(access_token):
    auth_val = 'Bearer %s' % access_token
    return {'Authorization': auth_val}

def get_account(access_token, api_uri):
    request_url = '%sv1/%s' % (api_uri, 'accounts')
    r = requests.get(request_url, headers=__build_auth_header(access_token))
    return r.json()['accounts'][0]['number']

def get_account_positions(access_token, api_uri, account_id):
    request_url = '%sv1/accounts/%s/positions' % (api_uri, account_id)
    r = requests.get(request_url, headers=__build_auth_header(access_token))
    print(r.json())

def get_streaming_port(access_token):
    request_url = '%sv1/markets/quotes?ids=4807280&stream=true&mode=WebSocket' % api_uri
    r = requests.get(request_url, headers=__build_auth_header(access_token))
    return r.json()['streamPort']

refresh_token = input('Please enter refresh token: ')
auth_response = __initialize_auth_request(refresh_token)
access_token = __get_access_token(auth_response)
api_uri = __get_api_uri(auth_response)

account_number = get_account(access_token, api_uri)
get_account_positions(access_token, api_uri, account_number)

streaming_port = get_streaming_port(access_token)

async def consume(message):
    print(message)

async def hello(access_token, streaming_port, api_uri):
    request_url = '%s:%i' % (api_uri[:-1], streaming_port)
    request_url = request_url.replace('https', 'wss')
    print("Connecting... %s" % request_url)
    async with websockets.connect(request_url) as websocket:
        print("> {}".format(access_token))
        await websocket.send(access_token)

        greeting = await websocket.recv()
        print("< {}".format(greeting))

        async for message in websocket:
            await consume(message)

asyncio.get_event_loop().run_until_complete(hello(access_token, streaming_port, api_uri))