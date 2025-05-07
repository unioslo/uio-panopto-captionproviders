#!python3

import os
import argparse
import requests
import urllib3
from common.folders_captionprovider import PanoptoFoldersCaptionprovider
from common.panopto_oauth2 import PanoptoOAuth2

def parse_argument():
    parser = argparse.ArgumentParser(description='Sample of Authorization as User Based Server Application')
    parser.add_argument('--server', dest='server', required=True, help='Server name as FQDN')
    parser.add_argument('--client-id-var', dest='client_id_var', default='PAN_CLIENT_ID', help='OS environment variable for Client ID of OAuth2 client')
    parser.add_argument('--client-secret-var', dest='client_secret_var', default='PAN_CLIENT_SECRET', help='OS environment variable for Client Secret of OAuth2 client')
    parser.add_argument('--username-var', dest='username_var', default='PAN_USERNAME', help='OS environment variable for username for script')
    parser.add_argument('--password-var', dest='password_var', default='PAN_PWD', help='OS environment variable for password')
    parser.add_argument('--start-folder-id', dest='start_folder_id', required=True, help='Initial folder ID')
    parser.add_argument('--provider-id', dest='provider_id', required=True, help='ID of the caption provider, use None to remove caption provider')
    parser.add_argument('--provider-name', dest='provider_name', required=True, help='Name of the caption provider, use None to remove caption provider')
    parser.add_argument('--skip-verify', dest='skip_verify', action='store_true', required=False, help='Skip SSL certificate verification. (Never apply to the production code)')
    return parser.parse_args()

def process_subfolders_inorder(panopto_folders, folder_id, provider_id, provider_name, level=0):
    """
    Recursively process children folders and their IDs.
    """
    children = panopto_folders.get_children(folder_id)
    #print('Child folder ID: {0} Child folder name:  {1}'.format(child['Id'], child['Name']))
    for child in children:
        print('Child folder ID: {0} Child folder name: {1} Level: {2}'.format(child['Id'], child['Name'], level))
        current_provider_id, current_provider_name = panopto_folders.get_folder_captionprovider(child['Id'])
        print('BEFORE: Caption provider ID: {0} Caption provider name: {1}'.format(current_provider_id, current_provider_name))
        if current_provider_id is None:
            # Set caption provider
            print('Setting caption provider ID: {0} Caption provider name: {1}'.format(provider_id, provider_name))
            panopto_folders.update_folder_captionprovider(child['Id'], provider_id, provider_name)
            id, name = panopto_folders.get_folder_captionprovider(child['Id'])
            print('AFTER: Caption provider ID: {0} Caption provider name: {1}'.format(id, name))
        process_subfolders_inorder(panopto_folders, child['Id'], provider_id, provider_name, level + 1)

def main():
    # Parse command line arguments and get client_id, client_secret, password and username from environment variables
    # Note: Not passed as command line arguments for security reasons.
    args = parse_argument()
    client_id = os.environ.get(args.client_id_var) # None if not set
    if client_id is None or client_id == '':
        print('error: Environment variable for client_id is not set {0}'.format(args.client_id_var))
        exit(1)
    client_secret = os.environ.get(args.client_secret_var) # None if not set
    if client_secret is None or client_secret == '':
        print('error: Environment variable for client_secret is not set {0}'.format(args.client_secret_var))
        exit(1)
    panopto_username = os.environ.get(args.username_var) # None if not set
    if panopto_username is None or panopto_username == '':
        print('error: Environment variable for Panopto username is not set {0}'.format(args.username_var))
        exit(1)
    panopto_password = os.environ.get(args.password_var) # None if not set
    if panopto_password is None or panopto_password == '':
        print('error: Environment variable for Panopto password is not set {0}'.format(args.password_var))
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
    oauth2 = PanoptoOAuth2(args.server, client_id, client_secret, not args.skip_verify)

    # Create PanoptoFoldersUB instance
    panopto_folders = PanoptoFoldersCaptionprovider(args.server, not args.skip_verify, oauth2, panopto_username, panopto_password)

    # Process all children folders
    process_subfolders_inorder(panopto_folders, args.start_folder_id, args.provider_id, args.provider_name)

if __name__ == '__main__':
    main()
