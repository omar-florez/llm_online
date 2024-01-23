from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import pdb

def configure():
  load_dotenv()

def call_search_engine(query):
  configure()
  serpapi_api_key = os.getenv('serpapi_api_key')
  params = {
    "q": query,
    # "location": "California, United States",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "api_key": serpapi_api_key,

  }

  search = GoogleSearch(params)
  return search.get_dict()