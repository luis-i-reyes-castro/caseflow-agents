#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from flask import Flask
from flask import request

from sofia_utils.printing import ( print_recursively,
                                   print_sep )
from wa_agents.basemodels import ( WhatsAppMsg,
                                   WhatsAppContact )
from wa_agents.whatsapp_functions import send_whatsapp_text


load_dotenv()
VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
print(f"WA_VERIFY TOKEN: {VERIFY_TOKEN}")


# Start Flask
app = Flask(__name__)

# --- Webhook verification (GET) ---
@app.route( "/webhook", methods = ["GET"])
def verify() :
    
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token == VERIFY_TOKEN:
        return challenge
    
    return "Verification failed", 403

# --- Handle incoming messages (POST) ---
@app.route( "/webhook", methods = ["POST"])
def webhook() :
    
    data = request.get_json()
    print( "Incoming:", data)
    
    try :
        changes  = data["entry"][0]["changes"][0]["value"]
        messages = changes.get( "messages", [])
        contacts = changes.get( "contacts", [])
        if not messages :
            return "no messages", 200
        
        contact = WhatsAppContact.model_validate(contacts[0])
        msg     = WhatsAppMsg.model_validate(messages[0])
        
        print_sep()
        print("CONTACT STRUCTURE:")
        print_recursively(contact)
        print_sep()
        print("MESSAGE STRUCTURE:")
        print_recursively(msg)
        
        MDJ_OPTS = { "indent"        : 4,
                     "by_alias"      : True,
                     "exclude_unset" : True,
                     "exclude_none"  : True}
        
        send_whatsapp_text( msg.user, msg.model_dump_json(**MDJ_OPTS))
        send_whatsapp_text( msg.user, contact.model_dump_json(**MDJ_OPTS))
    
    except Exception as e :
        print( "Error:", e)
    
    return "ok", 200

if __name__ == "__main__":
    app.run( port = 5000, debug = True)
