import msal
import webbrowser

def get_access_token_by_device_flow(params):
    app = msal.PublicClientApplication(
        client_id=params['client_id'],
        authority=params['authority_url']
    )

    flow = app.initiate_device_flow(params['scopes'])
    print(flow['user_code'])
    webbrowser.open(flow['verification_uri'])

    token = app.acquire_token_by_device_flow(flow)
    return token


def get_access_token_by_auth_code(params):
    app = msal.ConfidentialClientApplication(
        client_id=params['client_id'],
        client_credential=params['client_credentials'],
        authority=params['authority_url']
    )

    # create authorization url
    auth_url = app.get_authorization_request_url(
        scopes=params['scopes'],
        redirect_uri=params['redirect_uri'],
        response_type='code'
    )

    # open the authorization url in a web browser
    webbrowser.open(auth_url)

    # get authorization code from user input
    auth_code = input('Enter authorization code: ')

    # exchange authorization code for access token
    access_token = app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=params['scopes'],
        redirect_uri=params['redirect_uri']
    )

    return access_token


def connect_to_api(params):  # needed to rewrite to user auth flow

    access_token = get_access_token_by_device_flow(params)['access_token']
    #access_token = get_access_token_by_auth_code(params)['access_token']
    headers = {'Authorization': 'Bearer ' +
               access_token, 'ConsistencyLevel': 'eventual'}

    return headers
