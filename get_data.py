import requests
import os
import urllib
import config as cfg
import pandas as pd

os.chdir(os.path.expanduser('~/') + 'Code/data_science/CollegeProfile')
college_names = cfg.list_places 
key = cfg.api_key

get_id_base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
get_details_base_url = 'https://maps.googleapis.com/maps/api/place/details/json'
review_text = {}

#college_name = 'Massachusetts Institute of Technology'
for college_name in college_names:
    print(college_name)
    get_id_params = {'input' : college_name,
              'inputtype' : 'textquery',
              'fields' : 'place_id',
              'key' : key
             }
    get_id_param_encoded = urllib.parse.urlencode(get_id_params)
    id_response = requests.get(url=get_id_base_url, params=get_id_param_encoded)
    id_data = id_response.json()
    place_id = id_data['candidates'][0]['place_id']
   
    get_details_params = {'placeid' : place_id,
              'fields' : 'name,rating,review',
              'key' : key
            }
    get_details_param_encoded = urllib.parse.urlencode(get_details_params)
    details_response = requests.get(url=get_details_base_url, params=get_details_params)
    details_data = details_response.json()
    
    reviews = details_data['result']['reviews']
    text = []
    for review in reviews:
        text.append(review['text'])
        
    review_text[college_name] = text


review_text_dataframe = pd.DataFrame(review_text)
review_text_dataframe.to_csv('college_reviews.csv')
