from django.http import HttpResponse
import datetime 
from django.shortcuts import render

def home(request):
    isActive = True
    if request.method == 'POST':
        check = request.POST.get("check")
        print(check)
        if check is None: isActive=False
        else: isActive=True


    date = datetime.datetime.now()

    name = "LearnCodingWithDurgesh"
    list_of_programs = [
        'WAP to check even or odd',
        'WAP to check prime number',
        'WAP to print pascals triangle'
    ]

    student={
        "student_name": "Rahul",
        "student_college":"ZYZ",
        "student_city":"Lucknow"
    }
    print("test function is called from view")
    # return HttpResponse("<h1> Hello this is index page</h1>"+ str(date))

    data = {
        "date": date,
        "isActive": isActive,
        "name": name,
        "list_of_programs": list_of_programs,
        "student_data": student
    }

    return render(request, "home.html", data)

def about(request):
    # return HttpResponse("<h1> This is about page  </h1>")
    return render(request, "about.html", {})

def services(request):
    # return HttpResponse("<h1> This is services page  </h1>")
    return render(request, "services.html", {})