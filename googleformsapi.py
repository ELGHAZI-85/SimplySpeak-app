from oauth2client import client, file, tools
from apiclient import discovery
from httplib2 import Http

def create_form(ques, resp):
    
    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": "Machine Learning Quiz",
        }
    }

    # Request body to add a multiple-choice question
    
    NEW_QUESTION = {
        "requests": []
    }

    for i in range(len(ques)):
        question = ques[i]
        options = resp[i]

        create_item = {
            "createItem": {
                "item": {
                    "title": question,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": option} for option in options
                                ],
                                "shuffle": True
                            }
                        }
                    }
                },
                "location": {
                    "index": 0
                }
            }
        }

        NEW_QUESTION["requests"].insert(0,create_item)

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()
    responder_uri = result['responderUri']

    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()
    #print('Questions ', question_setting)
    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    #print('get-result',get_result)
    
    return responder_uri
