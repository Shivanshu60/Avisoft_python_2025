from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
from bs4 import BeautifulSoup
from apis.models import Paragraph
from django.http import HttpResponse
import re
from django.contrib import messages





def home(request):
    url = None  # To store the submitted URL
    error_message = None  # To store any error message
    paragraphs = []  # To store extracted paragraphs
    title=""
    ptag_db = Paragraph.objects.all()
    screenshot = None

    if request.method == "POST":
        url = request.POST.get("url")  # Retrieve the submitted URL
        request.session['url'] = url  # Temporarily store the URL in session

        try:
            # Validate the URL format
            validator = URLValidator()
            validator(url)

            # Fetch the URL content
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # paragraph data fetch 
                soup = BeautifulSoup(response.content, "html.parser")
                title = soup.title.string if soup.title else "No title found"
                paragraphs = [p.get_text() for p in soup.find_all("p")]

             


            else:
                error_message = f"URL returned status code {response.status_code}."
        except ValidationError:
            error_message = "Invalid URL format."
        except requests.RequestException as e:
            error_message = f"Failed to fetch URL: {e}"

    else:
        # Fetch the URL from the session if it's a GET request
        url = request.session.get('url', None)

    return render(
        request,
        "home.html",
        {
            "title": title,
            "url": url,  # Pass the URL to the template
            "paragraphs": paragraphs,
            "error_message": error_message,
            "ptag_db": ptag_db,
        },
    )

def save_para(request):
    if request.method == "POST":
        url = request.POST.get("url")

        # Fetch the URL content
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # paragraph data fetch 
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.string if soup.title else "No title found"
            paragraphs = [p.get_text() for p in soup.find_all("p")]


        # Save the list of formatted paragraphs into the database
        paragraph = Paragraph.objects.create(title=title, url=url, content=paragraphs)
        paragraph.save()

        # Add a success message
        messages.success(request, "Data saved successfully!")

        return redirect("/home/")  # Redirect to the home page after saving

    return render(request, "error.html", {
        "message": "Invalid Request",
        "data_saved": False,
    })



def view_para(request, id):
    pdata = Paragraph.objects.get(pk=id)

    return render(
        request,
        "view_paragraph.html",  # A new template for viewing a single paragraph
        {
            "pdata": pdata,
        }
    )

def download_para(request, id):
    # Retrieve the paragraph data from the database by the given ID
    try:
        pdata = Paragraph.objects.get(pk=id)
    except Paragraph.DoesNotExist:
        return HttpResponse("Paragraph not found", status=404)

    # Prepare the content to be written to the file
    content = f"Title: {pdata.title}\nURL: {pdata.url}\n\n"
    for para in pdata.content:
        if para.strip():  # Only add non-empty paragraphs
            content += f"Paragraph {pdata.content.index(para)+1}:\n{para}\n\n"
        else:
            content += f"Paragraph {pdata.content.index(para)+1}: Empty Paragraph\n\n"

    # Create the HttpResponse with the content as a text file
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{pdata.title}.txt"'
    
    return response

def delete_para(request, id):
    print(id)
    pdata = Paragraph.objects.get(pk=id)
    pdata.delete()
    return redirect("/home/")

def downloads(request):
    ptag_db = Paragraph.objects.all()
    return render(
        request,
        "downloads.html",
        {
            "ptag_db" : ptag_db
        }
    )


def about(request):
    return render(request, "about.html", {})







# Custom 404 error page view
def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)


