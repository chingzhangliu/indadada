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
  _token = msg.strip().split(" ")
  _low_token = _token[0].lower()
  if '!h' in _token[0]:
    _message=TextSendMessage(text="給個數字")
    line_bot_api.reply_message(event.reply_token, _message)
    reply =TextSendMessage(text="您所搜尋的結果為：\n")
    line_bot_api.reply_message(event.reply_token,reply)
  else:
    
    addr=event.reply_token
    profile = line_bot_api.get_profile(addr)
    reply =TextSendMessage(text=addr)
    line_bot_api.reply_message(event.reply_token,reply)
    rank=prk(int(_token[0]))
    for r in rank:
      result_message = r[0] + "("+r[1]+")"
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result_message))
    
def prk(num):
  result = []
  target = 'https://www.pixiv.net/ranking.php?mode=female'
  r = requests.get(target)
  soup=BeautifulSoup(r.text,'html.parser')
  res=soup.find('div',{'class':'ranking-items adjust'})
  res_rk=res.find_all('section',{'class':"ranking-item"})
  for idx, rk in enumerate(res_rk):
    if idx < num:
      tag=rk.find('h2').find('a')
      title=tag.get_text()
      href='https://www.pixiv.net/'+tag['href']
      result.append((title,href))
  return result
  
import os
if __name__=="__main__":
  
  port=int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)
