from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from .models import Project2
from .models import VideoInfo2

from json import dumps

from .yClient import YouTubeClient as yc, VideoInfo as vi

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import Project2Serializer
from .serializers import VideoInfo2Serializer

def createProject(request):
    if request.method == 'POST':
        title = request.POST.get('textfield', None)
        if(title != ""):
            customer = request.user
            proj = Project2(customer=customer,title=title)
            proj.save()
            print(proj)
            return render(request, 'base/project2.html', {"projects": proj})
        else:
            print("you must name a project")
            return redirect('/home')

def pro(request,pk):
    if(request.user.is_authenticated):
        customer = request.user
        if request.method == 'POST':
            search_term = request.POST.get('textfield', None)
            p = Project2.objects.get(id=pk)

            p.search_term = search_term
            p.not_objects = True
            p.save()
            if(len(VideoInfo2.objects.filter(project=p))>0):
                v = VideoInfo2.objects.filter(project=p)
                for i in v:
                    i.delete()
            Yclient = yc(search_term)
            print("Created Yclient")
            for video in Yclient.videoList:
                v = VideoInfo2(project=p,likes=video.likes,dislikes=video.dislikes,views=video.views,sentiment=video.analysis,date=video.date,tag=video.tags)                                                    
                v.save()
        
        p = Project2.objects.get(id=pk)
        if(p.customer != customer):
                return render(request,'base/error.html')
        data = []
        data.append(pk)
        data = dumps(data)
        return render(request,'base/project2.html',{"projects":p,"data":data})
    else:
        return render(request,'base/error.html')

@api_view(['GET'])
def thing(request,pk):
    p = Project2.objects.get(id=pk)
    video = VideoInfo2.objects.filter(project=p)
    serializer = VideoInfo2Serializer(video,many=True)
    
    return Response(serializer.data)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("base:home")
    return render(request, 'base/user_login.html')

def how(request):
    return render(request, 'base/howItWorks.html')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        project = Project2.objects.filter(customer=customer)
    else:
        return redirect("base:user_login")
    return render(request, 'base/home.html',{"projects":project})
    
def header(request):
    return render(request, 'base/header.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print("Got")
        if form.is_valid():

            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("base:home")


        else:
            for msg in form.error_messages:
                print(msg)
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "base/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "base/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("base:user_login")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("base:home")
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "base/user_login.html",
                    context={"form":form})

def deleteTask(request,pk):
    pro = Project2.objects.get(id=pk)
    pro.delete()
    return  redirect('/home')

