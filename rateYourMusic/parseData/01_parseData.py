#!usr/bin/env python3

import os
import glob
import codecs
import json
import re
import bs4
from tqdm import tqdm

def get_file_paths(folder):
    # Get all html file paths from a folder
    f_paths = glob.glob(os.path.join(folder, '*.html'))
    # Sort f_paths by id
    f_paths.sort(key=lambda x: int(re.search(r'\d+', x).group(0)))
    return f_paths

def parse_html(f_path):
    # Read file
    f = codecs.open(f_path, 'r')
    # Parse html
    html = bs4.BeautifulSoup(f.read(), 'html.parser')
    return html

# Define a function to handle Nonetype error:
# --- Non-existence tag when the value is empty
def handle_none(code):
    try:
        return eval(code)
    except (TypeError, AttributeError, KeyError, IndexError):
        return None

def parse_hyperlink(a_tags):
    # Declare all global variables for this function
    global a_tag
    
    # Check if there is at least one tag
    if len(a_tags) > 0:
        parsed = []
        for a_tag in a_tags:
            record = {
                'class': handle_none(code="a_tag['class'][0].strip()"),
                'href': handle_none(code="a_tag['href'].strip()"),
                'title': handle_none(code="a_tag['title'].strip()"),
                'text': handle_none(code="a_tag.text.strip()")
            }
            parsed.append(record)
        return parsed
    elif len(a_tags) == 0:
        return None

def parse_comment_href(a_tags):
    # Declare all global variables for this function
    global a_tag
    
    parsed = []
    for a_tag in a_tags:
        href = handle_none(code="a_tag['href'].strip()")
        parsed.append(href)
    return parsed

def parse_data(html, _id):
    # Declare all global variables for this function
    global K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11, K12, K13
    global K14, K15, K16, K17, K18, K19, K20, K21, K22, K23, K24, comment, a_tags
    
    # Header part
    K1 = {'V0': handle_none(code="html.select('ol.ui_breadcrumb li')[1].text.strip()")}
    K2 = {
        'V0': handle_none(code="list(html.find('td', text='For').next_siblings)[0].text.strip()"),
        'V1': [handle_none(code="list(html.find('td', text='For').next_siblings)[1].find('a').text.strip()"), 
                handle_none(code="list(html.find('td', text='For').next_siblings)[1].find('a')['href']")],
        'V2': handle_none(code="list(html.find('td', text='For').next_siblings)[2].text.strip()")
    }
    
    # Summary part
    # -- Submitted by
    K3 = {
        'V0': [handle_none(code="re.search(r'(.+) send PM', html.find('td', text='Submitted by').next_sibling.text)[1].strip()"),
                handle_none(code="html.find('td', text='Submitted by').next_sibling.find('a')['href']")]
    }
    # -- Submit Time
    K4 = {'V0': handle_none(code="html.find('td', text='Submit Time').next_sibling.text.strip()")}
    # -- Approval Status
    K5 = {
        'V0': handle_none(code="html.find('td', text='Approval Status').next_sibling.text.strip()"),
        'V1': [handle_none(code="html.find('td', text='Approval Status').next_sibling.find('a').text.strip()"), 
                handle_none(code="html.find('td', text='Approval Status').next_sibling.find('a')['href']")]
    }
    # -- Comments
    K6 = {'V0': handle_none(code="html.find('td', text='Comments').next_sibling.text.strip()")}
    # -- Votes
    K7 = {
        'V0': handle_none(code="re.search(r'.+?(?=;)', html.find('td', text='Votes').next_sibling.text)[0].strip()"),
        'V1': handle_none(code="re.search(r'Yes:.+?(?=;)', html.find('td', text='Votes').next_sibling.text)[0].strip()"),
        'V2': handle_none(code="re.search(r'Hold:.+?(?=;)', html.find('td', text='Votes').next_sibling.text)[0].strip()"),
        'V3': handle_none(code="re.search(r'No:.+', html.find('td', text='Votes').next_sibling.text)[0].strip()")
    }
    
    # Details part
    # -- Request Type
    K8 = {'V0': handle_none(code="html.select_one('table:not([class]) h4').text.strip()")}
    
    # Specify the variable names for K10 to K20
    var_names = {
        'K10': 'First Name',
        'K11': 'Last Name',
        'K12': 'genre ID',
        'K13': 'AKAs',
        'K14': 'Parent genre',
        'K15': 'Can be rated on a scale',
        'K16': 'Top level',
        'K17': 'Is category only',
        'K18': 'Type',
        'K19': 'description_short',
        'K20': 'description',
        'K21': 'Meta comments'
    }
    
    # There are two patterns depending on the `Request type (K8)`
    # if K8['V0'] == 'Edit' (ex. 51392) or 'Delete' (ex. 10100): There will be values for both `V0` and `V1`
    # if K8['V0'] == 'New' (ex. 42616): V1 for all fields will be NULL
    # For K9
    # -- Contributor
    K9 = {
        'V0': [handle_none(code="list(html.find('td', text='Contributor').next_siblings)[0].text.strip()"),
                handle_none(code="list(html.find('td', text='Contributor').next_siblings)[0].find('a')['href']")],
        'V1': [handle_none(code="list(html.find('td', text='Contributor').next_siblings)[1].text.strip()"),
                handle_none(code="list(html.find('td', text='Contributor').next_siblings)[1].find('a')['href']")]
    }
    
    # For K10 to K21
    for key, value in var_names.items():
        globals()[key] = {
            'V0': handle_none(code=f"list(html.find('td', text='{value}').next_siblings)[0].text.strip()"),
            'V1': handle_none(code=f"list(html.find('td', text='{value}').next_siblings)[1].text.strip()")
        }
    
    # For K22 - Hyperlink in the description (K20)
    # --- This could be `genre` or `artist` mentioned in the description.
    # Check if K20 contains any description
    if K20['V0'] is not None:
        a_tags = handle_none(code="list(html.find('td', text='description').next_siblings)[0].find_all('a')")
        K22 = {'V0': parse_hyperlink(a_tags)}
    elif K20['V0'] is None:
        K22 = {'V0': None}
    
    if K20['V1'] is not None:
        a_tags = handle_none(code="list(html.find('td', text='description').next_siblings)[1].find_all('a')")
        K22['V1'] = parse_hyperlink(a_tags)
    elif K20['V1'] is None:
        K22['V1'] = None
    
    # For K23 - Hyperlink in the Meta comments (K21)
    # Check if K21 contains any meta comment
    if K21['V0'] is not None:
        a_tags = handle_none(code="list(html.find('td', text='Meta comments').next_siblings)[0].find_all('a')")
        K23 = {'V0': parse_hyperlink(a_tags)}
    elif K21['V0'] is None:
        K23 = {'V0': None}
    
    if K21['V1'] is not None:
        a_tags = handle_none(code="list(html.find('td', text='Meta comments').next_siblings)[1].find_all('a')")
        K23['V1'] = parse_hyperlink(a_tags)
    elif K21['V1'] is None:
        K23['V1'] = None
    
    # For K24 - Comments
    comments = html.find_all('div', {'class': 'comment'})
    comment_list = []
    for comment in comments:
        a_tags = handle_none(code="comment.find('div', {'class': 'commentbody'}).find_all('a')")
        comment_list.append(
            {
                'V0': handle_none(code="comment.find('a').text.strip()"),
                'V1': handle_none(code="comment.find('a')['href']"),
                'V2': handle_none(code="comment.find('div', {'class': 'commentbody'}).text.strip()"),
                'V3': handle_none(code="parse_comment_href(a_tags)"),
                'V4': handle_none(code="re.search(r'([a-z]):', comment.find('div', {'class': 'comment_vote_date'}).text)[1].strip()"),
                'V5': handle_none(code="re.sub(r'[a-z]:', '', comment.find('div', {'class': 'comment_vote_date'}).text).strip()")
                }
        )
    K24 = comment_list
    
    # Structure a record
    record = {}
    record['thread_id'] = _id
    keys = [f'K{i}' for i in range(1, 24 + 1)]
    for key in keys:
        record[key] = globals()[key]
    
    return record

def main():
    # Get all file paths
    f_paths = get_file_paths(folder='threads')
    # Remove invalid html page: 'threads/51371.html'
    invalid_f = 'threads/51371.html'
    f_paths.remove(invalid_f)
    # Open output file for 'write'
    with open('output.json', 'w') as f:
        _json = []
        for f_path in tqdm(f_paths):
            # Extract id
            _id = re.search(r'\d+', f_path).group(0)
            # Parse html
            global html
            html = parse_html(f_path)
            # Parse data
            record = parse_data(html, _id)
            # Store data
            _json.append(record)
        # Write data
        json.dump(_json, f)

if __name__ == "__main__":
    main()