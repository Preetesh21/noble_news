from django.http import HttpResponse
from django.shortcuts import render
from news.site_checker import checker
from news.google_search import start_predict
from news.article_checker import predict

def index(request):
    if(request.POST):
        if 'ArticleS' in request.POST:
            print("Article")
            screenname = request.POST.get("Article", None)
            if(screenname==''):
                return render(request,'output.html',{'output':'No words'})
            text2csv(screenname)
            display=predict('news\\data.csv')
            if(display<0):
                display=0.001
            display=str(('%0.2f' % display))+" % True"
            return render(request, 'output.html' ,{'output': display})
        elif 'KeyWordS' in request.POST:
            screenname1 = request.POST.get("KeyWord", None)
            print(screenname1)
            if(screenname1==''):
                return render(request,'output.html',{'output':'No words'})
            predict1=start_predict(screenname1)
            predict1=float(predict1)*100
            predict1=str(predict1)+" % True"
            print(predict1)
            return render(request, 'output.html' ,{'output': predict1})
        else:
            screenname2 = request.POST.get("Website", None)
            predict2 = checker(screenname2)
            print(predict2)
            return render(request, 'output.html' ,{'output': predict2})
        return render(request,'output.html')
        #return HttpResponse("Helllo")
    return render(request,'index.html')


def text2csv(screenname):
    t=""
    data_file = open("news\\data.csv", 'w')
    for s in screenname:
       if(s!=',' and s!='\n'):
           t=t+s
    data_file.write('text, \n'+t+',')
