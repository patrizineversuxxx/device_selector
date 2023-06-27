import typing
import msal
import webbrowser


def get_access_token_by_device_flow(connection_parameters: typing.Dict) -> typing.Dict:
    app = msal.PublicClientApplication(
        client_id=connection_parameters['client_id'],
        authority=connection_parameters['authority_url']
    )

    flow = app.initiate_device_flow(connection_parameters['scopes'])
    print(flow['user_code'])
    webbrowser.open(flow['verification_uri'])

    token = app.acquire_token_by_device_flow(flow)
    return token

def get_access_token_silent(connection_parameters: typing.Dict) -> typing.Dict:
    app = msal.ConfidentialClientApplication(
        client_id=connection_parameters['client_id'],
        #client_credential=connection_parameters['client_credentials'],
        client_credential={"thumbprint": connection_parameters['thumbprint'], "private_key": open(connection_parameters['private_key_file']).read()},
        authority=connection_parameters['authority_url']
    )

    #token = None
    token = app.acquire_token_silent(connection_parameters['scope'], account=None)
    if token is None:
        token = app.acquire_token_for_client(scopes=connection_parameters['scope'])
    return token
    

def get_access_token_by_auth_code(connection_parameters: typing.Dict) -> typing.Dict:
    app = msal.ConfidentialClientApplication(
        client_id=connection_parameters['client_id'],
        client_credential={"thumbprint": connection_parameters['thumbprint'], "private_key": open(connection_parameters['private_key_file'].read())},
        authority=connection_parameters['authority_url']
    )

    # create authorization url
    auth_url = app.get_authorization_request_url(
        scopes=connection_parameters['scopes'],
        redirect_uri=connection_parameters['redirect_uri'],
        response_type='code'
    )

    # open the authorization url in a web browser
    webbrowser.open(auth_url)

    # get authorization code from user input
    auth_code = input('Enter authorization code: ')

    # exchange authorization code for access token
    access_token = app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=connection_parameters['scopes'],
        redirect_uri=connection_parameters['redirect_uri']
    )

    return access_token


# needed to rewrite to user auth flow
def connect_to_api(connection_parameters: typing.Dict) -> typing.Dict:

    access_token = get_access_token_silent(connection_parameters)

    if access_token is None:
        access_token = get_access_token_by_device_flow(
        connection_parameters)['access_token']
    else:
        access_token = access_token['access_token']

    headers = {'Authorization': 'Bearer ' +
               access_token, 'ConsistencyLevel': 'eventual'}

    return headers
