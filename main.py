import os

from flask import Flask, jsonify, request
from itsdangerous import json
from twilio.twiml.messaging_response import MessagingResponse, Media,Message
from google.cloud import dialogflow
from fpdf import FPDF
import json
import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

path = Path('./pdfs/one.pdf')
xy = os.path.abspath(path)

pdf = FPDF()
# Add a page
pdf.add_page()
pdf.set_font("Arial", size = 15)

cloudinary.config(cloud_name="gicheworks", api_key="248314148666268", api_secret="vQAEKDhMrXCu0jJXWpixEr9N0iE")
# create a cell
pdf.cell(200, 10, txt = "Techcamp Kenya", 

         ln = 1, align = 'C')
  

 
# from google.protobuf.json_format import MessageToJson, MessageToDict

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "botconfig.json"

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

    print("Query text: {}".format(response.query_result.query_text))

    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    import proto

    json_string = proto.Message.to_json(response)
    return json_string

######## do not touch#####

# @app.route('/')
# def hello_world():
#     return jsonify({
#    "response":"true"
# })

@app.route('/')
def false():
    return  jsonify({
   "response":"false"
})


######## do not touch#####

@app.route("/sms", methods=["POST"])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    msg = request.form.get("Body")
    x = request.form.get("Media")
    print('this is my x', x)
    
    dialogflowResponse = detect_intent_texts(PROJECT_ID, "thisismysessionid", msg, "en")
    
    # storing name and email of user
    # name:str 


    result = json.loads(dialogflowResponse)

    if len(result['queryResult']['parameters'].keys()) > 0: 
        # print(result['queryResult']['parameters'].keys())

        name:str = result['queryResult']['parameters']['name']
        email:str = result['queryResult']['parameters']['email']
        if name and email:
            print('i am here', name , email)
            logging.info('Saving user to students database')
            # generating pdf
            # add another cell
            pdf.cell(200, 10, txt = f"Hey {name}, this is your Application letter",
                    ln = 2, align = 'C')
            
            # save the pdf with name .pdf
            pdfx = pdf.output(f"./pdfs/{name}.pdf") 
            resp = MessagingResponse()
            print(pdfx,'pdf')
            message =  Message()
      
              

            pdfResult = cloudinary.uploader.upload(f'pdfs/{name}.pdf', public_id=f'admission-Letters/{name}')
            # print('this is my img var', pdfResult)
            
            message.body('Here is your apllicition letter')
            message.media(pdfResult['secure_url'])
            resp.append(message)
        
            return str(resp)

    resp = MessagingResponse()
    # this is sending response to user
    resp.message(result['queryResult']['fulfillmentText'])

    return str(resp)


@app.route("/flow", methods=["POST", "GET"])
def flow_reply():
    x = detect_intent_texts(PROJECT_ID, "123456789", "payments", "en")
    print("hey flow", x)
    return "je"


if __name__ == "__main__":
    app.run(debug=True)
