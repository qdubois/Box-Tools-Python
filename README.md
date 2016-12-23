# Box-Tools-Python

## What can you do with it:
Recursively scan a box folder and get a list of all the file.
You can also download them.

## How to use it:
You'll need to create a Box dev APP and get you secret key and client id.
Token will be generated for the first time and stored securely.

You'll need to have :
 - boxsdk
 - wsgiref
 - keyring
 - bottle
 installed.

## Sample call:
python box_utils.py download MY_FOLDER_NAME
or
python box_utils.py info PERSO


