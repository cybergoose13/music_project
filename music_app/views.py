from django.shortcuts import render

# login should be the landing page of localhost:8000/
# 
def login(request):
    context={

    }
    return render(request, 'login.html', context)

def register(request):
    return render(request, 'register.html')