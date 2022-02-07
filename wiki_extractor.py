# To run this program : 
# python wiki_extractor.py --keyword=”Indian Historical Events” --num_urls=100 --output=”out.json”

import requests 
from bs4 import BeautifulSoup
import json
import sys

# Counter 't' Just for console output purpose
t = 0 
# List 'urls' to store all the urls
urls = []
# List 'paragraphs' to store all the paras extracted 
paragraphs = []

try:
    # 'key_word' stores the input from user (string argument to define the query string). Ex."Indian Historical events"
    key_word = sys.argv[1].split('=')[1]   
    key_word = "+".join(key_word.split(" "))    # "Indian+Historical+events"

    # 'num_urls' stores the input from user (integer argument for number of wikipedia pages to extract from). Ex.100
    num_urls = sys.argv[2].split('=')[1]    
    
    # Creating url with user inputs such as key_word and num_urls and wikipedia domain name.
    url = "https://en.wikipedia.org/w/index.php?title=Special:Search&limit="+str(num_urls)+"&offset=0&profile=default&search="+key_word+"&ns0=1"
    
    # Getting the entire source code of the url.
    response = requests.get(url)    
    requests.session().close()

    # Parsing the 'response' content to HTML format.
    soup = BeautifulSoup(response.content , "html.parser")  

    # Finding all the div tags from the html page that contains the attribute value for class as 'mw-search-result-heading'.
    related_urls = soup.find_all("div", attrs = {"class":"mw-search-result-heading"})

    # Iterating through all the div tags 
    for r_url in related_urls:
        # generating the url for individual search result.
        # By getting 'a' child-tag of div. 
        r_url = "https://en.wikipedia.org"+r_url.findChild("a")['href']
        
        t += 1  # Counter increment
        print( t, r_url) # Console output

        # Adding the generated url to the 'urls' list.
        urls.append(r_url)

        # Getting the entire source code of the generated url.
        r_url_response = requests.get(r_url)
        requests.session().close()

        # Parsing the 'r_url_response' content to HTML format.
        r_soup = BeautifulSoup(r_url_response.content , "html.parser")

        # Finding the div tag from the html page that contains the attribute value for class as 'mw-parser-output'.
        related_para = r_soup.find("div", attrs = {"class":"mw-parser-output"})

        # 'para_content' to store the text of paragraphs.
        para_content = ""        
        c = 0   # Counter for extracting 2 paras from the web page.

        # Iterating through all the 'p' tags in response of the div tag "related_para".
        for p in related_para.findChildren("p"):            
            if( c < 2 ):
                # Checking does the 'p' tag contains enough chars to be said as the paragraph.
                if len(p.getText()) >= 255 :
                    para_content += p.getText() + "\n"
                    c += 1
            else:
                break
        
        # Adding the extracted paragraph contents to the 'paragraphs' list.
        paragraphs.append(para_content)

    # 'file_name' stores the input from user for output filename. Ex."out.json"
    file_name = sys.argv[3].split('=')[1] 
    # Opening a json file in write mode.
    with open( file_name , 'w') as file:
        # Adding data into the json file from the "urls" and "paragraphs" list.
        json.dump(  [{'url': u, 'paragraph': para} for u, para in zip(urls, paragraphs)] , file , indent=4)        
    print("Done")

except Exception as e:
    print(e)