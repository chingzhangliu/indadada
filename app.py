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
from selenium import webdriver

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
    _message=TextSendMessage(text="給個數字?")
    line_bot_api.reply_message(event.reply_token, _message)
  elif '茶湯會' in _token[0]:
    img=ImageSendMessage(
    original_content_url='https://twcoupon.com/images/menu/p_teapatea_2017_5_n.jpg',
    preview_image_url='https://twcoupon.com/images/menu/p_teapatea_2017_5_n.jpg'
    )
    line_bot_api.push_message(event.source.user_id, img)
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text='https://tw.tp-tea.com/news/ins.php?index_id=121'))
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text='https://tw.tp-tea.com/news/ins.php?index_id=106'))
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text='https://tw.tp-tea.com/news/ins.php?index_id=101'))
  else:
    
    addr=event.reply_token
    
    reply =TextSendMessage(text=event.source.user_id)
    line_bot_api.reply_message(event.reply_token,reply)
    
    shop  findshop(int(_token[0]))
    for r in shop:
      result_message = r[0] + "("+r[1]+")"
      line_bot_api.push_message(event.source.user_id, TextSendMessage(text=result_message))
    
def findshop(num):
  result = []
  target = 'https://www.google.com.tw/maps/search/%E9%A3%B2%E6%96%99%E5%BA%97/@24.180978,120.5990928,15z/data=!4m3!2m2!5m1!10e2'
  driver = webdriver.PhantomJS(executable_path= '/phantomjs-2.1.1-windows/bin')
  driver.get(target)
  pageSource = driver.page_source
  soup=BeautifulSoup(pageSource,'lxml')
  res=soup.find('jsl').find('div',{'id':'content-container'}).find('div',{'id':"pane"}).find('div',{'role':'listbox'}).find('div',{'role':'listbox'})
  res_all=res.find_all('div',{'class':'section-result'})
  for idx, ls in enumerate(res_all):
    if idx < num:
      name=ls.find('h3').get_text()
      rate=ls.find('span',{'class':'section-result-rating'}).get_text()
      loc=ls.find('span',{'class':'section-result-location'}).get_text()
      result.append((name,rate,loc))
    
  return result
  
import os
if __name__=="__main__":
  
  port=int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)
