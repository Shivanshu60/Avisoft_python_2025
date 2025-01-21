import requests
from bs4 import BeautifulSoup

def fetchAndSaveToFile(url, path):
    # Fetch the content from the URL
    r = requests.get(url)
    # Save the content to the specified file path
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI"
file_path = "temp.html"

# Fetch the webpage and save it to a file
fetchAndSaveToFile(url, file_path)

# Open the file and parse its contents
with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract all <div> tags
all_divs = soup.find_all("p")

print(all_divs)
# # Print the total number of divs and the first few as an example
# print(f"Total <div> tags found: {len(all_divs)}")
# print(all_divs[:3])  # Print the first 3 <div> tags as a preview

# for link in soup.find_all("a"):
#     print(link.get("href"))
#     print(link.get_text())

# s = soup.find(id="link3")
# print(s.get("href"))

s =