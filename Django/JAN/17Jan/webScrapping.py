import requests

def fetchAndSaveToFile(url, path):
    r = requests.get(url)
    # Specify utf-8 encoding when writing to the file
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://en.wikipedia.org/wiki/Grand_Theft_Auto_VI"
fetchAndSaveToFile(url, "data/times.html")
