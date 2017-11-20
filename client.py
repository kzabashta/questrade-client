import requests

OAUTH_SERVICE_URL = 'https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token='

def __initialize_auth_request(refresh_token):
    r = requests.get(OAUTH_SERVICE_URL + refresh_token)
    print(r)
    return r.json()

def __get_access_token(auth_response):
    return auth_response['access_token']

def __get_api_uri(auth_response):
    return auth_response['api_server']

def __build_auth_header(access_token):
    auth_val = 'Bearer %s' % access_token
    return {'Authorization': auth_val}

def get_accounts(access_token, api_uri):
    request_url = '%sv1/%s' % (api_uri, 'accounts')
    r = requests.get(request_url, headers=__build_auth_header(access_token))
    print(r)

refresh_token = input('Please enter refresh token: ')
auth_response = __initialize_auth_request(refresh_token)
access_token = __get_access_token(auth_response)
api_uri = __get_api_uri(auth_response)

print(get_accounts(access_token, api_uri))
