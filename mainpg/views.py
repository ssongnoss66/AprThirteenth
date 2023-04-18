from django.shortcuts import render

# Create your views here.
def mainpg(request):
    return render(request, 'mainpg/mainpg.html')