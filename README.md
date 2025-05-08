# uio-panopto-captionproviders

Scripts to set captionprovider for folders using the Panopto REST API

## Authorization as User Based Server Application
These scripts are authorized based on User Based Server Application. User Based Server Application is not recommended in general, because the application needs to handle the user's password directly. For some types of scripts, that is OK as long as the machine running the scripts is secure.

Most of authorization logic is in common code: [panopto_oauth2.py](common/panopto_oauth2.py).

## Preparation
1. You need a Panopto user account. It needs to be an Administrator account for the CaptionProviders API
2. If you do not have Python 3 on your system, install the latest stable version from https://python.org. (Tested with Python 3.11.)
3. Install external modules for this application.
```
pip install requests oauthlib requests_oauthlib
```

## Setup API Client on Panopto server
1. Sign in to the Panopto web site
2. Click the System icon at the left-bottom corner.
3. Click API Clients
4. Click New
5. Enter an arbitrary Client Name
6. Select User Based Server Application type.
7. Enter ```https://localhost``` into CORS Origin URL.
8. The rest can be blank. Click "Create API Client" button.
9. Note the created Client ID and Client Secret.

## Prepare the environment variables 

These are the default environment variable names.

Type the following commands (Linux).

```
export PAN_CLIENT_ID=some_client_id
export PAN_CLIENT_SECRET=some_client_secret
export PAN_USERNAME=some_username
export PAN_PWD=some_password
```

## Run the captionproviders script to list available captionproviders

Type the following command:

```
python captionproviders.py --server [Panopto server name] 

```
This displays the list of caption providers in the instance. 
Note that this script must currently be run as an `Administrator` user to access the list of caption providers.

## Run the captionprovider_for_folders script to set captionprovider where it is not set

Type the following command:

```
python captionprovider_for_folders.py --server [Panopto server name] --start-folder-id [Folder ID to start] --provider-id [ID of provider to set] --provider-name [Name (not DisplayName) of provider to set]
```
This sets the caption provider for child folders (and their children folders recursively) in the instance starting from the `--start-folder-id` folder (if the caption provider it is not already set).
Note that the script does not currenlty modify the `--start-folder-id` folder itself, only its children.
This script can be run as a user with `Videographer`+ `Caption Requester` access.


## License
Copyright 2025 The University of Oslo

Based on and includes portions of https://github.com/Panopto/panopto-api-python-examples,  which is Copyright 2019 Panopto

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
