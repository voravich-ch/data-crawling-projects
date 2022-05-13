import scrapy
from itemloaders.processors import MapCompose, Compose, Join, TakeFirst
import re
import pycountry
import bs4
import numpy as np
import pandas as pd
import datetime
from urllib.parse import urljoin

def parse_beer_stats(item_list):
    if item_list:
        output = {
            "Average": item_list[0].strip(),
            "Beers": item_list[1].strip(),
            "Ratings": item_list[2].strip()
        }
        return output

def parse_place_stats(item_list):
    if item_list:
        output = {
            "Average": item_list[0].strip(),
            "Ratings": item_list[1].strip(),
            "pDev": item_list[2].strip()
        }
        return output

def parse_location(item_list):
    if item_list:
        # Clean text
        item_list = list(map(lambda i: i.replace(',', '').strip(), item_list))
        # Get all countries in the world to parse location
        countries = [country.name for country in list(pycountry.countries)]
        # Add some countries with different names
        countries.extend(['Czech Republic'])
        # Find index where the country name is located (End of location address)
        l = list(map(lambda i: i in countries, item_list))
        if sum(l) > 0:
            idx = l.index(True)
            location = item_list[2:idx+1]
            location = list(filter(None, location))
            location = ', '.join(location)
            return location

def parse_phone_number(item_list):
    if item_list:
        # Find index that contains phone number
        regex1 = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        regex2 = r'[\d\s-]{8,}[0-9]'
        regex = re.compile(f'{regex1}|{regex2}')
        l = list(map(lambda i: bool(regex.match(i)), item_list))
        if sum(l) > 0:
            idx = l.index(True)
            # Extract phone number
            phone_number = regex.match(item_list[idx]).group(0)
            return phone_number

def parse_notes(item_list):
    if item_list:
        # Find index that contains "Notes:"
        l = ['Notes:' in elem for elem in item_list]
        if sum(l) > 0:
            idx = l.index(True)
            # Extract notes
            notes = item_list[idx:]
            notes = ''.join(notes).replace('Notes:', '').strip()
            return notes

def parse_company_name(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = {
            "text": html.find('b', text='From:').find_parent('dt').find_next_sibling('dd').find('a').get_text(),
            "href": html.find('b', text='From:').find_parent('dt').find_next_sibling('dd').find('a')['href']
        }
        return output
    except:
        return None

def parse_style(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = {
            "text": html.find('b', text='Style:').find_parent('dt').find_next_sibling('dd').find('a').get_text(),
            "href": html.find('b', text='Style:').find_parent('dt').find_next_sibling('dd').find('a')['href']
        }
        return output
    except:
        return None
    
def parse_ABV(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('b', text='ABV:').find_parent('dt').find_next_sibling('dd').find('span').get_text()
        return output
    except:
        return None
    
def parse_score(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('b', text='Score:').find_parent('dt').find_next_sibling('dd').find('span').get_text()
        return output
    except:
        return None
def parse_avg(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('b', text='Avg:').find_parent('dt').find_next_sibling('dd').find('b').get_text()
        return output
    except:
        return None
    
def parse_pDev(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('span', {'class': re.compile(r'^ba-pdev')}).get_text()
        return output
    except:
        return None
    
def parse_ratings(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('b', text='Ratings:').find_parent('dt').find_next_sibling('dd').find('b').get_text()
        return output
    except:
        return None
    
def parse_status(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('span', text='Status:').find_parent('dt').find_next_sibling('dd').find('span').get_text()
        return output
    except:
        return None
    
def parse_date_added(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    try:
        output = html.find('span', text='Added:').find_parent('dt').find_next_sibling('dd').find('span').get_text()
        return output
    except:
        return None
    
def parse_author(a_tag):
    html = bs4.BeautifulSoup(a_tag, 'html.parser')
    try:
        output = {
            "name": html.find('a').get_text(),
            "href": html.find('a')['href']
        }
        return output
    except:
        return None
    
def parse_assessment(item_list):
    if item_list:
        # Clean text; format as list -> to dataFrame -> to dict
        text = item_list[0]
        l = text.split(' | ')
        l = [i.split(':') for i in l]
        df = pd.DataFrame(l).set_index(0)
        output = df.to_dict()[1]
        return output

def parse_review_text(item_list):
    if item_list:
        # Find index that contains text (Between author_location and post_date)
        regex_author_loc = r'^ from .+$'
        regex_date = r'^\w{3} \d+, \d{4}$'
        regex = re.compile(f'{regex_author_loc}|{regex_date}')
        l = list(map(lambda i: bool(regex.match(i)), item_list))
        if sum(l) > 0:
            # Extract review
            review = list(np.array(item_list[l.index(True):])[~np.array(l[l.index(True):])])
            review = ''.join(review)
            review = review.replace('\u00a0\u00a0Report', '')
            return review

def parse_joined_date(text):
    # Clean text
    text = text.strip()
    # If text is in the date format
    regex_date = re.compile(r'^\w{3} \d+, \d{4}$')
    if regex_date.match(text):
        return text
    else:
        # Parse day of the week to date
        if text == "Today": 
            return datetime.datetime.now().strftime('%d/%m/%Y')
        elif text == "Yesterday":
            return (datetime.datetime.now()-datetime.timedelta(1)).strftime('%d/%m/%Y')
        elif text == (datetime.datetime.now()-datetime.timedelta(2)).strftime("%A"):
            return (datetime.datetime.now()-datetime.timedelta(2)).strftime('%d/%m/%Y')
        elif text == (datetime.datetime.now()-datetime.timedelta(3)).strftime("%A"):
            return (datetime.datetime.now()-datetime.timedelta(3)).strftime('%d/%m/%Y')
        elif text == (datetime.datetime.now()-datetime.timedelta(4)).strftime("%A"):
            return (datetime.datetime.now()-datetime.timedelta(4)).strftime('%d/%m/%Y')
        elif text == (datetime.datetime.now()-datetime.timedelta(5)).strftime("%A"):
            return (datetime.datetime.now()-datetime.timedelta(5)).strftime('%d/%m/%Y')
        elif text == (datetime.datetime.now()-datetime.timedelta(6)).strftime("%A"):
            return (datetime.datetime.now()-datetime.timedelta(6)).strftime('%d/%m/%Y')

def parse_info_beers(item_list):
    if item_list:
        # Initialise output
        output = {}
        # Clean data
        item = ''.join(item_list)
        # Parse output
        fields = ['Ratings', 'Added', 'Brewers', 'Beer Styles', 'US States', 'Countries', 'Wants', 'Gots', 'Photos']
        for field in fields:
            # Extract number
            regex_num = re.compile(f'{field}: ([\d,]+)')
            output[field] = regex_num.search(item).group(1)
        return output

def parse_info_places(item_list):
    if item_list:
        # Initialise output
        output = {}
        # Clean data
        item = ''.join(item_list)
        # Parse output
        fields = ['Ratings', 'Added', 'Brewers', 'Bars/Eateries', 'Stores', 'US States', 'Countries', 'Photos']
        for field in fields:
            # Extract number
            regex_num = re.compile(f'{field}: ([\d,]+)')
            output[field] = regex_num.search(item).group(1)
        return output

def parse_about(item_list):
    if item_list:
        # Initialise output
        output = {}
        # Clean data
        item_list = list(map(lambda i: i.strip(), item_list))
        item_list = [i for i in item_list if i]
        item = ' '.join(item_list)
        # Parse output
        fields = ['Gender', 'Birthday', 'Age', 'Location']
        output = {
            "Gender": re.search(r'Gender: (\w+)', item).group(1) if re.search(r'Gender', item) else None,
            "Birthday": re.search(r'Birthday: ([\w\s,]+)', item).group(1).strip() if re.search(r'Birthday', item) else None,
            "Age": re.search(r'Age: (\d+)', item).group(1) if re.search(r'Age', item) else None,
            "Location": re.search(r'Location: (\w+)', item).group(1) if re.search(r'Location', item) else None,
            "text": '\n'.join(item_list)
        }
        return output

def parse_forum_atag(item):
    a_tag = bs4.BeautifulSoup(item, 'html.parser')
    base_url = 'https://www.beeradvocate.com/community/'
    output = {
        "text": a_tag.get_text(strip=True),
        "href": urljoin(base_url, a_tag.find('a')['href'])
    }
    return output

def parse_n_likes(item):
    html = bs4.BeautifulSoup(item, 'html.parser')
    # Find if there are more likes than it can show; e.g., "and 13 others"
    if html.select('a[class=OverlayTrigger]'):
        num_others = int(re.search(r'\d+', html.select_one('a[class=OverlayTrigger]').get_text()).group())
        total_likes = num_others + len(html.select('a[class=username]'))
    else:
        total_likes = len(html.select('a[class=username]'))
    return total_likes

def parse_comment(items):
    if items:
        items = [item.strip() for item in items if bool(item.strip())]
        return '\n'.join(items)
    
def parse_quote(items):
    if items:
        output = []
        for item in items:
            html = bs4.BeautifulSoup(item, 'html.parser')
            if html.select('div[class*=attribution]'):
                comment_id = re.search(r'.+#(post-\d+)', html.select_one('div[class*=attribution] a')['href']).group(1)
            else:
                # This is just a normal blockquote which is not related to any previous comments
                comment_id = None
            text = html.select_one('div[class=quote]').get_text()
            document = {
                "comment_id": comment_id,
                "text": text
            }
            output.append(document)
        return output

class beerAdvocateCrawlItem(scrapy.Item):
    # PlaceMetadata fields
    name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    type = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    location = scrapy.Field(input_processor=Compose(parse_location), output_processor=TakeFirst())
    gmap = scrapy.Field(output_processor=TakeFirst())
    is_active = scrapy.Field(output_processor=TakeFirst())
    stats = scrapy.Field(input_processor=Compose(parse_place_stats), output_processor=TakeFirst())
    beer_stats = scrapy.Field(input_processor=Compose(parse_beer_stats), output_processor=TakeFirst())
    phone_number = scrapy.Field(input_processor=Compose(parse_phone_number), output_processor=TakeFirst())
    website = scrapy.Field(output_processor=TakeFirst())
    notes = scrapy.Field(input_processor=Compose(parse_notes), output_processor=TakeFirst())
    
    # BeerMetadata fields
    # name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    company = scrapy.Field(input_processor=MapCompose(parse_company_name), output_processor=TakeFirst())
    style = scrapy.Field(input_processor=MapCompose(parse_style), output_processor=TakeFirst())
    ABV = scrapy.Field(input_processor=MapCompose(parse_ABV, str.strip), output_processor=TakeFirst())
    score = scrapy.Field(input_processor=MapCompose(parse_score, str.strip), output_processor=TakeFirst())
    avg = scrapy.Field(input_processor=MapCompose(parse_avg, str.strip), output_processor=TakeFirst())
    pDev = scrapy.Field(input_processor=MapCompose(parse_pDev, str.strip), output_processor=TakeFirst())
    ratings = scrapy.Field(input_processor=MapCompose(parse_ratings, str.strip), output_processor=TakeFirst())
    status = scrapy.Field(input_processor=MapCompose(parse_status, str.strip), output_processor=TakeFirst())
    date_added = scrapy.Field(input_processor=MapCompose(parse_date_added, str.strip), output_processor=TakeFirst())
    # notes = scrapy.Field(input_processor=Compose(parse_notes), output_processor=TakeFirst())
    
    # PlaceReview + BeerReview fields
    place = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    beer = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    author = scrapy.Field(input_processor=MapCompose(parse_author), output_processor=TakeFirst())
    date = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    rDev = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    assessment = scrapy.Field(input_processor=Compose(parse_assessment), output_processor=TakeFirst())
    text = scrapy.Field(input_processor=Compose(parse_review_text), output_processor=TakeFirst())
    
    # UserMetadata fields
    # name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    status = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    tags = scrapy.Field(input_processor=MapCompose(str.strip))
    joined_date = scrapy.Field(input_processor=MapCompose(parse_joined_date), output_processor=TakeFirst())
    posts_done = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    likes_received = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    beer_karma = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    info_beers = scrapy.Field(input_processor=Compose(parse_info_beers), output_processor=TakeFirst())
    info_places = scrapy.Field(input_processor=Compose(parse_info_places), output_processor=TakeFirst())
    about = scrapy.Field(input_processor=Compose(parse_about), output_processor=TakeFirst())
    n_follower = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    n_following = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    
    # UserFollower + UserFollowing fields
    focal = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    followers = scrapy.Field()
    followings = scrapy.Field()
    
    # Forum fields
    forum = scrapy.Field(input_processor=MapCompose(parse_forum_atag), output_processor=TakeFirst())
    thread_url = scrapy.Field(output_processor=TakeFirst())
    thread_topic = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    thread_starter = scrapy.Field(input_processor=MapCompose(parse_forum_atag), output_processor=TakeFirst())
    thread_start_date = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    author = scrapy.Field(input_processor=MapCompose(parse_forum_atag), output_processor=TakeFirst())
    comment = scrapy.Field(input_processor=Compose(parse_comment), output_processor=TakeFirst())
    comment_id = scrapy.Field(output_processor=TakeFirst())
    comment_date = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    comment_order = scrapy.Field(input_processor=MapCompose(lambda i: re.search(r'\d+', i).group()), output_processor=TakeFirst())
    quotes = scrapy.Field(input_processor=Compose(parse_quote))
    n_likes = scrapy.Field(input_processor=MapCompose(parse_n_likes), output_processor=TakeFirst())
    
    # Housekeeping fields
    response_url = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())
    crawl_date = scrapy.Field(output_processor=TakeFirst())