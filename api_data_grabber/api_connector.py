import typing
import msal


def get_access_token_silent(connection_parameters: typing.Dict) -> typing.Dict:
    """
    Retrieves an access token using the MSAL library with the silent flow.

    Args:
        connection_parameters (typing.Dict): A dictionary containing connection parameters.
            - client_id (str): The client ID for the application.
            - thumbprint (str): The thumbprint of the private key.
            - private_key_file (str): Path to the private key file.
            - authority_url (str): The authority URL for authentication.
            - scope (str): The scope for the access token.

    Returns:
        typing.Dict: The token information containing access token and other details.
    """
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


def connect_to_API(connection_parameters: typing.Dict) -> typing.Dict:
    """
    Connects to an API using the provided connection parameters.

    Args:
        connection_parameters (typing.Dict): A dictionary containing connection parameters.
            - See get_access_token_silent() docstring for details.

    Returns:
        typing.Dict: Headers containing the authorization token.
    """
    access_token = get_access_token_silent(
        connection_parameters).get("access_token")

    headers = {'Authorization': 'Bearer ' +
               access_token, 'ConsistencyLevel': 'eventual'}

    return headers
