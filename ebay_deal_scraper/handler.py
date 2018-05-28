import boto3
import json
import requests
from bs4 import BeautifulSoup
import datetime

top_deal_selector = '.ebayui-dne-item-featured-card--topDeals'
title_selector = '.dne-itemtile-title'
price_selector = '.dne-itemtile-price'
discount_selector = '.dne-itemtile-original-price'

def scrape(event, context):
  data = deal_scrape()
  file_name = f"deals-{data['date']}"
  save_file_to_s3('ebay-daily-deals', file_name, data)

def deal_scrape():
  page = requests.get("https://www.ebay.com/deals")
  content = BeautifulSoup(page.content, 'html.parser')
  deal = content.select(top_deal_selector)[0]
  item = deal.select(title_selector)[0].get_text()
  price = deal.select(price_selector)[0].get_text()
  discount = deal.select(discount_selector)[0].get_text()
  return {
    'date': str(datetime.datetime.now()),
    'price': price,
    'item': item,
    'discount': discount
  }

def save_file_to_s3(bucket, file_name, data):
  s3 = boto3.resource('s3')
  obj = s3.Object(bucket, file_name)
  obj.put(Body=json.dumps(data))

