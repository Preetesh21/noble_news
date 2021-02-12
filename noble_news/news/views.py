from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    print(request)
    if(request.POST):
        print(request.POST)
        return render(request,'output.html')
        #return HttpResponse("Helllo")
    return render(request,'index.html')