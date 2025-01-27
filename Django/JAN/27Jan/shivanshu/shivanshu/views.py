from django.http import HttpResponse
from django.shortcuts import render
from .forms import usersForm



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

def submitForm(request):
    pass

def userForm(request):
    finalans = 0
    fn = usersForm()

    data = {'form': fn}


    return render (request, "userForm.html", data)

def calculator(request):
    c= ''
    try:
        if request.method == "POST":
            n1 = eval(request.POST.get('num1'))
            n2 = eval(request.POST.get('num2'))
            opr = request.POST.get('opr')

            if opr == '+':
                c=n1+n2
            elif opr == '-':
                c = n1-n2
            elif opr == '*':
                c = n1*n2
            elif opr == '/':
                c = n1/n2


        
    except:
        c = "Invalid operation"
    # print(c)
    return render(request, "calculator.html", {'c': c})


