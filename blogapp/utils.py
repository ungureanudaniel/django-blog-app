#scraping imports
import requests
from bs4 import BeautifulSoup
import json
import re


#fetch instagram followers of artisan bakery
def insta_followers_count():
    instagram_url = 'https://www.instagram.com'
    profile_url = 'artisanbakerybrasov'
    response = requests.get(f"{instagram_url}/{profile_url}")
    #print(response.status_code)
    if response.ok:
        bs_html = BeautifulSoup(response.text, "html.parser")
        #print(response.text)
        scripts = bs_html.select('script[type="application/ld+json"]')
        script_content = json.loads(scripts[0].string.extract())
        #print(json.dumps(script_content, indent=4, sort_keys=True))
        main_entity_of_page = script_content['mainEntityofPage']
        interaction_statistic = main_entity_of_page['interactionStatistic']
        insta_followers_count = interaction_statistic['userInteractionCount']
    return insta_followers_count

def fb_followers_count():
    facebook_url = 'https://www.facebook.com'
    profile_url = 'artisanbakerybrasov'
    response = requests.get(f"{facebook_url}/{profile_url}")
        #print(response.status_code)
    if response.ok:
        bs_html = BeautifulSoup(response.text, "html.parser")
        regex = re.compile('^_4bl9')
        content_list = bs_html.find_all('div', attrs={'class': regex})
        content = []
        for div in content_list:
            content.append(div.get_text().split('\n')[0])
        followers_text = content[2].split()
        followers = followers_text[0]

    return followers
