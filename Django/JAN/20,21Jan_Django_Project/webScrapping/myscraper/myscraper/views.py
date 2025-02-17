import requests
from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup


def scrape_ptags(request):
    validator = URLValidator()
    url = request.POST.get("url")
    extracted_text = None
    error_message = None

    if request.method == "POST":

        try:
            validator(url)     
        except ValidationError:
            error_message = "Invalid URL. Please enter a valid link."
            return render(request, "form.html", {"error": error_message})

        try:
            response = requests.get(url, timeout=5)  
            response.raise_for_status()  

            # Parse HTML and extract <p> tags
            soup = BeautifulSoup(response.text, "html.parser")
            extracted_text = [p.get_text(strip=True) for p in soup.find_all("p")]

        except requests.exceptions.RequestException as e:
            error_message = f"Failed to fetch URL: {str(e)}"

    return render(request, "form.html", {"extracted_text": extracted_text, "error": error_message})
          


