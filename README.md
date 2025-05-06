# uio-panopto-captionproviders

Scripts to set captionprovider for folders using the Panopto REST API

## Authorization as User Based Server Application
These scripts are authorized based on User Based Server Application. User Based Server Application is not recommended in general, because the application needs to handle the user's password directly. For some types of scripts, that is OK.

Most of authorization logic is in common code: [panopto_oauth2.py](common/panopto_oauth2.py).

## Preparation
1. You need a Panopto user account.
2. If you do not have Python 3 on your system, install the latest stable version from https://python.org. (Tested with Python 3.11.)
3. Install external modules for this application.
```
pip install requests oauthlib requests_oauthlib
```
TODO: Other required modules?

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

## Run the captionproviders script to list available captionproviders

Export the password to OS variable chosen for password, e.g. for Linux:

```
export THE_PANOPTO_PWD=somepassword
```

Type the following command:

```
python captionproviders.py --server [Panopto server name] --client-id [Client ID] --client-secret [Client Secret] --username [User name] --password-var [Name of OS variable with password]

```
This displays the list of caption providers in the instance. 
Note that this script must run as an admin user to access the list of caption providers.

## Run the captionprovider_for_folders script to set captionprovider where it is not set

Export the password to OS variable chosen for password (if not already done), e.g. for Linux:

```
export THE_PANOPTO_PWD=somepassword
```

Type the following command:

```
python captionprovider_for_folders.py --server [Panopto server name] --client-id [Client ID] --client-secret [Client Secret] --username [User name] --password-var [Name of OS variable with password] --start-folder-id [Folder ID to start] --provider-id [ID of provider to set] --provider-name [Name (not DisplayName) of provider to set]
```
This displays the list of caption providers in the instance. 
Note that this script must run as an admin user to access the list of caption providers.


## License
Copyright 2024 UiO

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
