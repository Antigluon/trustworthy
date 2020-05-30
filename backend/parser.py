import requests
import json
from bs4 import BeautifulSoup

class Strip():

    def __init__(self, link):
        """Accepts an article link and attempts to parse it into text and article data"""
        url = "https://api.outline.com/v3/parse_article?source_url={}".format(link)
        payload = {}
        headers = {
        'referer': 'https://outline.com/'
        }
        response = requests.request("GET", url, headers=headers, data = payload).json()
        self.resp = response

    def raw_text(self):
        """Extracts the raw text from the provided article link and returns it, clean of html tags
        and javascript"""
        soup = BeautifulSoup(self.resp['data']['html'], 'lxml')
        return soup.get_text()
    
    def pretty_json(self):
        """Returns the extracted data from the article as a pretty json element easy to read"""
        return json.dumps(self.resp, indent=2, sort_keys=True)
    
    def raw_response(self):
        """Get the full response of all data extracted from the article as a python dict to parse
        and grab any other data that doesn't have its own function"""
        return self.resp
    
    def is_success(self):
        """Check that this is true before calling any other functions, if it failed to extract text and
        data, this will be false and you can return to the extension that it couldn't find content to 
        fact-check."""
        return self.resp["success"] and self.resp['data']['html'] is not None and self.resp['data']['language'] == 'en'
        
    def article_title(self):
        """Returns the extracted article title"""
        return self.resp['data']['title']
    
    def site_name(self):
        """Returns the extracted article site name. Ex: CNN, Fox News, etc"""
        return self.resp['data']['site_name']

    def domain_name(self):
        """Returns the domain name of the inputted news article"""
        return self.resp['data']['domain']
    
    def author(self):
        """Attempts to find and return the author of the inputted news article"""
        return self.resp['data']['author']
    
    def read_time(self):
        """Returns the article's estimated read time"""
        return self.resp['data']['read_time']
    
    def date(self):
        """Returns the date published/modified of the article"""
        return self.resp['data']['date']
    
    def keywords(self):
        """Attempts to find and extract keywords from the article"""
        return self.resp['data']['keywords']
