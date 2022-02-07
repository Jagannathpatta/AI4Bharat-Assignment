import pytesseract
from pdf2image import convert_from_bytes
from pytesseract import image_to_string
import pandas as pd
import json
from urllib.request import Request, urlopen
import requests 
from bs4 import BeautifulSoup

# Important line to handel the erros related to "pytesseract" the path is where the tesseract was installed.
# While installing tesseract please make sure to check mark for the additional language scripts.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_Text( path_to_pdf , language = "eng" ):
    """
    @desc: this function extracts text from the PDF.    
    @params:
        - path_to_pdf: URL of the pdf file to extract the content.
        - language: script language of the pdf.
    @returns:
        - the list of textual content of entire pdf, page wise [(1,"..."),...].
    """    
    try:
        # Getting the entire source code of the pdf_url.
        req = Request(path_to_pdf , headers={'User-Agent': 'Mozilla/5.0'})    
        
        # "convert_from_bytes" is method of pdf2image package used here for reading the individual pages of the pdf,
        # and converting them into list of "images".
        images = convert_from_bytes( urlopen(req).read() , poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
        
        file_data = []  # Empty list to store the contents to return.

        # Iterating through each image.
        for pg, img in enumerate(images):
            # Adding (page no. , contents) to the "file_data" list.
            # "image_to_string" is method of "pytesseract" package used here for extracting text form Image.
            file_data.append((pg ,  image_to_string( img , lang=language)))                
            
        return file_data
    except Exception as e:
        return None 

def get_reqURL( url ):
    """
    @desc: 'Scraping' this function extracts download pdf url from the given url.    
    @params:
        - url: URL of the pdf viewrer where is file located to extract the content.        
    @returns:
        - download url for a pdf file.
    """   
    try:
        response = requests.get(url)
        requests.session().close()

        soup = BeautifulSoup(response.content , "html.parser")

        related_urls = soup.find_all("a", attrs = {"class":"format-summary download-pill"})

        for r_url in related_urls:
            if "PDF" in r_url.getText() and ".pdf" in r_url["href"] :
                # print(r_url["href"] , r_url.getText())
                req_url = "https://archive.org" + r_url["href"]
                break
        return req_url
    except Exception as e:
        return None

# List 'output' to store all the dicts. 
output = []
# Counter 'c' Just for console output purpose
c = 0
try:
    # Reading the CSV file containing all the links.
    data = pd.read_csv("Data Engineer Task - Data Engineer Task.csv" , header= None) 
    # Counter 't' to store total no. of links, Just for console output purpose
    t = data.shape[0]

    # Iterating through all the links in the 'data'.
    for url in data[0]:
        print( "Please wait ",round((c / t)*100),"%")

        # list "res" to store the (page no. , contents) of the pdf.
        res = []

        # if the link is a proper url of the pdf.
        if url[-4:] == ".pdf" :     
            
            res = pdf_to_Text(url , language="mar")
                    
            for row in res:
                output.append({ 'page-url': url,
                                'pdf-url': url,
                                'pdf-content': row[1]  
                            })

        # if the link is not a proper url of the pdf.        
        else:
            # Scraping for the download url of the pdf.
            req_url = get_reqURL(url)            
            res = pdf_to_Text(req_url , language="mar")
                  
            url_chunks = url.split("/page/")
            pg_url = url_chunks[0] + "/page/n"
            if res :
                for row in res:
                    output.append({ 'page-url': pg_url+ str(row[0]) + "/mode/1up",
                                    'pdf-url': req_url,
                                    'pdf-content': row[1]  
                                })
            else:
                output.append({ 'page-url': pg_url+"0/mode/1up",
                                    'pdf-url': "PDF URL not Found",
                                    'pdf-content': "PDF content Not Found"  
                                })
        c = c+1    

    # Opening a json file in write mode.
    with open( "pdf_extract.json" , 'w' , encoding='utf8') as file:
        # Adding data into the json file from the "output" list.
        json.dump(  output , file , ensure_ascii=False ,indent=4)
    print("Done")
except Exception as e:
    print(e)