import requests
import json
import os
import sys
import argparse
from dotenv import load_dotenv

def shorten_link(token, url):
  if not url.startswith("https://"):
    if not url.startswith("http://"):
      url = f'https://{url}'

  request_url = 'https://api-ssl.bitly.com/v4/bitlinks'
  auth_header = f'Bearer {token}'
  headers = {
    "Authorization": auth_header
    }
  payload = {
    "long_url" : url
    }
  response = requests.post(request_url, headers=headers, json=payload)
  response.raise_for_status()
  bitlink = response.json()['id']
  return bitlink

def count_clicks(token, bitlink):
  request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
  auth_header = f'Bearer {token}'
  headers = {
    "Authorization": auth_header
    }
  payload = {
    "unit" : "day",
    "units" : "-1"
    }
  response = requests.get(request_url, headers=headers, params=payload)
  response.raise_for_status()
  clicks_count = response.json()['total_clicks']
  return clicks_count

if __name__ == '__main__':
  load_dotenv()
  token = os.getenv("BITLY_TOKEN")
  parser = argparse.ArgumentParser()
  parser.add_argument("url")
  args = parser.parse_args()
  url = args.url

  if url.startswith("bit.ly"):
    try:
      print(f'Number of shortened url clicks: {str(count_clicks(token, url))}')
    except requests.exceptions.HTTPError:
      print('Wrong bitlink')
  else:
    try:
      print(shorten_link(token, url))
    except requests.exceptions.HTTPError:
      print('Wrong url')