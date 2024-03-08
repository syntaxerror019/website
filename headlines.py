from flask import Flask, jsonify, Blueprint
import requests
from datetime import datetime, timezone
from newsapi import NewsApiClient
import re

news_blueprint = Blueprint('news', __name__)

# Replace 'YOUR_API_KEY' with your actual News API key
newsapi = NewsApiClient(api_key='13c4604d073c428c9258e4ab9f637bf4')


@news_blueprint.route('/')
def index():
    json_data = []
    top_headlines = newsapi.get_top_headlines(country="us", language="en")
    data = {"count": len(top_headlines['articles'])}
    json_data.append(data)
    for article in top_headlines['articles']:
        non_ascii_pattern = re.compile(r'[^\x00-\x7F]+')
        article_content = non_ascii_pattern.sub('', article['title'])
        data = {"headline": article_content}
        json_data.append(data)
        
     
    return jsonify(json_data)

# Print the headlines

