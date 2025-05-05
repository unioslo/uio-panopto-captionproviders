#!python3

import os
import argparse
import requests
import urllib3

from common.panopto_oauth2 import PanoptoOAuth2

def parse_argument():
    parser = argparse.ArgumentParser(description='Sample of Authorization as User Based Server Application')
    parser.add_argument('--server', dest='server', required=True, help='Server name as FQDN')
    parser.add_argument('--client-id', dest='client_id', required=True, help='Client ID of OAuth2 client')
    parser.add_argument('--client-secret', dest='client_secret', required=True, help='Client Secret of OAuth2 client')
    parser.add_argument('--username', dest='username', required=True, help='Username for OAuth2 Resource Owner Grant, must be admin for this API')
    parser.add_argument('--password-var', dest='password_var', required=True, help='OS environment variable name for password')
    parser.add_argument('--skip-verify', dest='skip_verify', action='store_true', required=False, help='Skip SSL certificate verification. (Never apply to the production code)')
    return parser.parse_args()

def main():
    # Parse command line arguments and get password from environment variable
    # Note: Password is not passed as command line argument for security reasons.
    args = parse_argument()
    panopto_password = os.environ.get(args.password_var) # None if not set
    if panopto_password is None or panopto_password == '':
        print('error: Environment variable for password is not set {0}'.format(args.password_var))
        exit(1)

    if args.skip_verify:
        # This line is sometimes needed to suppress annoying warning message. Do not use
        print('Warning: SSL certificate verification is skipped. Never apply to the production code.')
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Use requests module's Session object in this example.
    # ref. https://2.python-requests.org/en/master/user/advanced/#session-objects
    requests_session = requests.Session()
    requests_session.verify = not args.skip_verify
    
    # Load OAuth2 logic
    oauth2 = PanoptoOAuth2(args.server, args.client_id, args.client_secret, not args.skip_verify)
    
    # Initial authorization
    authorization(requests_session, oauth2, args.username, panopto_password)

    # Call Panopto API (geting caption providers with paging)
    # Note: CAlling this API currently requires admin role.
    providers = []
    page_number = 0
    print('Calling GET /api/v1/captionproviders endpoint')
    while True:
        url = 'https://{0}/Panopto/api/v1/captionproviders?pageNumber={1}'.format(args.server, page_number)
        resp = requests_session.get(url = url)
        if inspect_response_is_retry_needed(resp):
            continue
        data = resp.json()
        if len(data) == 0:
            break
        for provider in data:
            providers.append(provider)
        page_number += 1
    
    print()
    print('Caption providers:')
    for provider in providers:
        print('Enabled: {0} Id: "{1}" Name: "{2}" Display: "{3}"'.format(provider['Enabled'], provider['Id'], provider['Name'], provider['DisplayName']))

def authorization(requests_session, oauth2, username, password):
    # Go through authorization
    access_token = oauth2.get_access_token_resource_owner_grant(username, password)
    # Set the token as the header of requests
    requests_session.headers.update({'Authorization': 'Bearer ' + access_token})

def inspect_response_is_retry_needed(response):
    """
    Inspect the response of a requests' call, and return True if the response was Unauthorized.
    An exception is thrown at other error responses.
    Reference: https://stackoverflow.com/a/24519419
    """
    if response.status_code // 100 == 2:
        # Success on 2xx response.
        return False
        
    if response.status_code == requests.codes.unauthorized:
        print('Unauthorized. Access token is invalid.')
        return True

    if response.status_code == 429:
        print('Too many requests. Wait one sec, and retry.')
        time.sleep(1)
        return True

    # Throw unhandled cases.
    response.raise_for_status()


if __name__ == '__main__':
    main()
