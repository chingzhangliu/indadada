from flask import Flask, request, abort

import urllib.request, json
import requests
from bs4 import BeautifulSoup

import os, sys
from linebot import(
  LineBotApi, WebhookHandler
)
from linebot.exceptions import(
  InvalidSignatureError
)
from linebot.models import *

app=Flask(__name__)

ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
SECRET= os.environ['CHANNEL_SECRET']

line_bot_api=LineBotApi(ACCESS_TOKEN)
handler=WebhookHandler(SECRET)

@app.route("/")
def hello_world():
  return "hello world!"
  

@app.route("/callback", methods=['POST'])
def callback():
  signature=request.headers['X-Line-Signature']
  body=request.get_data(as_text=True)
  app.logger.info("Request body: "+body)
  try:
    handler.handle(body,signature)
  except InvalidSignatureError:
    abort(400)
    return 'OK'
  
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  msg=event.message.text
  _low_msg=msg.lower()
  locmsg=event.message.location
  _token=msg.strip().split(" ")
  _low_token=_token[0].lower()
  message = {
      type: 'text',
      text: reply_text
    } 
  line_bot_api.reply_message(event.reply_token, message)
  if '!h' in _token[0]:
    _message=TextSendMessage(text="1")
    line_bot_api.reply_message(event.reply_token, _message)
import os
if __name__=="__main__":
  
  port=int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)
