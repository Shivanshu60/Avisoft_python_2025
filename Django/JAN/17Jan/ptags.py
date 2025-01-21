import requests
from bs4 import BeautifulSoup

def scrape_paragraphs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    paragraph_texts = [p.get_text(strip=True) for p in paragraphs]
    return paragraph_texts

# URL 
url = "https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI"


paragraphs = scrape_paragraphs(url)


for i, paragraph in enumerate(paragraphs, 1):
    print(f"Paragraph {i}:")
    
    # Check for empty paragraphs 
    if paragraph.strip():  
        print(paragraph)
    else:
        print("Empty Paragraph!!!")
    
    print("-" * 80)
