import typing
import msal
import webbrowser


def get_access_token_silent(connection_parameters: typing.Dict) -> typing.Dict:
    app = msal.ConfidentialClientApplication(
        client_id=connection_parameters['client_id'],
        client_credential={"thumbprint": connection_parameters['thumbprint'], "private_key": open(
            connection_parameters['private_key_file']).read()},
        authority=connection_parameters['authority_url']
    )

    token = app.acquire_token_silent(
        connection_parameters['scope'], account=None)
    if token is None:
        token = app.acquire_token_for_client(
            scopes=connection_parameters['scope'])
    return token


# needed to rewrite to user auth flow
def connect_to_api(connection_parameters: typing.Dict) -> typing.Dict:

    access_token = get_access_token_silent(
        connection_parameters).get("access_token")

    headers = {'Authorization': 'Bearer ' +
               access_token, 'ConsistencyLevel': 'eventual'}

    return headers
