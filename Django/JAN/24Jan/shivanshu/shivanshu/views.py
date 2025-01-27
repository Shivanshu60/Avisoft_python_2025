from django.http import HttpResponse
from django.shortcuts import render

def homePage(request):
    data = {
        "title": 'Home Page',
        'bdata': 'ye views se aarha h',
        'clist': ['python', 'c++', 'c', 'Java'],
    }

    return render(request, "index.html", data)

def aboutUs(request):
    return render(request, "about.html")


def course(request):
    return HttpResponse('This is course page')

# for dynamic routing 
# int, str, slug (hello-world-hehe) dash separated data 

def courseDetail(request, courseid):
    return HttpResponse(courseid)

