import requests
import json
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from parser import Strip

with open("credentials.txt") as f:
  API_KEY = f.readline()

class Summarizer:
  def __init__(self):
    self.auto_abstractor = AutoAbstractor()
    self.auto_abstractor.tokenizable_doc = SimpleTokenizer()
    self.auto_abstractor.delimiter_list = [".", "\n"]
    self.abstractable_doc = TopNRankAbstractor()
    
  def summarize(self, document):
    result_dict = self.auto_abstractor.summarize(document, self.abstractable_doc)
    return [sentence.strip() for sentence in result_dict["summarize_result"]]

summarizer = Summarizer()

def fact_check(text):
  """search for stuff and fact check it"""
  summary_list = summarizer.summarize(text)
  payload = {'key': API_KEY, 'page_size': '1', 'query': summary_list[0]}
  r = requests.get('https://factchecktools.googleapis.com/v1alpha1/claims:search', params=payload)
  fc_raw = r.json()
  if not fc_raw:
    return {}
  fc_data = fc_raw['claims'][0]
  fc_review = fc_data['claimReview'][0]
  fc_source = Strip(fc_review['url'])
  fc_body = fc_source.raw_text()
  response = {
    'claim':fc_data['text'], 
    'by':fc_data['claimant'], 
    'fc_publisher':fc_review['publisher']['name'], 
    'fc_url': fc_review['url'],
    'fc_rating': fc_review['textualRating'],
    'fc_summary': ' '.join(summarizer.summarize(fc_body))
  }

  return response
  #return {"claim":"Typewriter", "rating":"Hamlet", "publisher":"Monkeys", "url":"https://factorfiction.online"}
