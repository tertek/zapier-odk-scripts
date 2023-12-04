# only python core imports available within zapier code action
# no external modules/packages allowed, except requests
import io
import sys
import csv
import base64
import requests
import json 

# scenario config
use_form_attachment = True # Set to True if you want to use form attachments

# base config
username = ""
password = ""
baseurl = "" # e.g. "https://odk-central-testing.swisstph.ch"
project = "" # e.g. "47"

# form config
form_register = "test_form_register" #name of form that is used for registration 
form_follow = "test_form_follow"  # name of form that is used for follow up
# if use_form_attachment
form_follow_attached = "test_form_follow_attached" # name of form that is used for follow up; 
form_attachment = "follow.csv" # name of form attachment attached to form_follow; 

# field config
field_email_register = "email_register" # name of email field for registration form
field_email_follow = "email_follow"
field_email_follow_attach = "email"

fields_additional = ["firstname", "lastname"]

# validate config
if not username or not password:
    raise Exception("username and password required")
if not baseurl or not project:
    raise Exception("baseurl and project required")

# auth config 
credentials_string = username+":"+password
credentials_bytes  = credentials_string.encode('ascii')
base64_bytes = base64.b64encode(credentials_bytes)
auth_token = base64_bytes.decode('ascii')

# helpers

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def odk_get(url):
    headers = {'Authorization': 'Basic '+ auth_token}
    payload = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        # in case we have a json response, there might be an error..
        if is_json(response.text):
            res = json.loads(response.text)
            if 'code' in res and res['code'] != "200":
                raise Exception(res["message"])

        return response.text

    except Exception as e:
        print("Error during ODK API call to:\n" + url)
        print(e)
        sys.exit()

# urls
url_auth = baseurl + "/v1/projects" + "/" + project

url_form_register = url_auth + "/forms" + "/" + form_register + "/submissions.csv"
url_form_follow   = url_auth + "/forms" + "/" + form_follow + "/submissions.csv"

# if use_form_attachment:
url_form_follow_attached = url_auth + "/forms" + "/" + form_follow_attached + "/attachments" + "/" + form_attachment

# validate API auth endpoint
response_auth = odk_get(url_auth)
response_auth_json = json.loads(response_auth)
if 'code' in response_auth_json:
    raise Exception(response_auth_json["message"])
if not str(response_auth_json['id']) == project:
    raise Exception("Invalid authentication config")

#
# methods
#
def list_emails(url, field):
    emails = []
    data = odk_get(url)
    f = io.StringIO(data)
    cr = csv.DictReader(f, delimiter=',')    
    for row in cr:
        emails.append(row[field])
    return emails

def get_registered_emails():
    if use_form_attachment:
       url = url_form_follow_attached
       field = field_email_follow_attach
    else:
        url = url_form_register
        field = field_email_register
    return list_emails(url, field)

def get_responding_emails():
    url = url_form_follow
    field = field_email_follow

    return list_emails(url, field)

def get_diff(registered, responding):
    emails = []
    for email in registered:
        if email not in responding:
            emails.append(email)
    return emails


# main
registered = get_registered_emails()
responding = get_responding_emails()
non_responding = get_diff(registered, responding)

# return output dict object to zapier action interface
output = {
    'registered': registered,
    'responding': responding,
    'non_responding': non_responding
    }

# # used during development
print(output)
