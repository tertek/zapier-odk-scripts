# zapier-odk-scripts
Written for Zapier Python Action
**External Libraries cannot be used**

## Disclaimer
The code has been written procedural and may be fully rewritten in order to keep configuration simple.

## get non responding

Get non-responding participants, based on two scenarios:
1) using CSV attachment as source for participant data
2) using registration form as source for participant data

The scripts fetches particpant data via ODK Central API, to calculate the difference between registered and responding participants, in context of a follow up form. Finally, based on the difference a list of non-respondents will be generated that can be used within Zapier for sending Emails or another action to fetch more data before sending emails.

### Setup
Define base configuration for the script:

```python
    # base config
    username = "username"
    password = "password"
    base =  "address-to-your-odk-central"
    project = "project-id"
```

..