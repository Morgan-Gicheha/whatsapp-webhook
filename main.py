
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import dialogflow



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'botconfig.json'

PROJECT_ID = "mytestbot-aufk"
# PROJECT_ID = "small-talk-camy"

app = Flask(__name__)





def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""


    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

   
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )


    # print("Query text: {}".format(response.query_result.query_text))
    # print(
    #     "Detected intent: {} (confidence: {})\n".format(
    #         response.query_result.intent.display_name,
    #         response.query_result.intent_detection_confidence,
    #     )
    # )
    # print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text



@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    msg = request.form.get('Body')
   
    dialogflowResponse = detect_intent_texts(PROJECT_ID,'thisismysessionid',msg,'en')
    print(dialogflowResponse)
    # dialogflowResponse = request.get_json(force=True)
    # print('..' * 50)
    # print(dialogflowResponse)
    resp = MessagingResponse()
    resp.message(dialogflowResponse)


    return str(resp)

@app.route("/flow", methods=['POST','GET'])
def flow_reply():
    x = detect_intent_texts(PROJECT_ID, '123456789', 'payments','en')
    print('hey flow',x)
    return 'je'


if __name__ == "__main__":
    app.run(debug=True)