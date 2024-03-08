from flask import Flask, jsonify, Blueprint, request
import requests
from datetime import datetime, timezone
import g4f

ai_blueprint = Blueprint('ai', __name__)

g4f.debug.logging = False  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking
#print(g4f.Provider.Bing.params)  # Print supported args for Bing
    
@ai_blueprint.route('/')
def index():
    return "only api for now!"

@ai_blueprint.route('/hacking_is_not_a_crime',  methods=['POST'])
def call():    
    conversation = request.json  # Access form data sent in the POST request
    
    if conversation is None:
        return "please specify a conversation", 418
    
    response = g4f.ChatCompletion.create(
      model=g4f.models.gpt_4,
      messages=conversation,
      provider=g4f.Provider.You,
    )  
    print(response)
    return response
  

