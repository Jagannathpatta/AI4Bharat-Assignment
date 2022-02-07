# Web Scraped PDF OCR

## To Run task 1
Step 1 : Install the requirements.txt file
pip install -r requirements.txt
Step 2 : Run the "wiki_extractor.py" file with inputs.
python wiki_extractor.py --keyword=”Indian Historical Events” --num_urls=100 --output=”out.json”

## To Run task 2
Step 1: tesseract must be installed on your system.
- While installing tesseract please make sure to check mark for the additional language scripts.
- Keep a note of path where the tesseract was installed.
- Edit the "FinalPdfExtract.py" file at line no. 12, replace the path with your tesseract install path.
Step 2: "poppler-0.68.0" must be installed on your system.
- Download the poppler-0.68.0.
- Extract the download and paste the folder on this Path "C:\Program Files\"
Step 3 : Install the requirements.txt file
pip install -r requirements.txt
Step 4 : Run the "FinalPdfExtract.py" file with inputs.
python FinalPdfExtract.py 
