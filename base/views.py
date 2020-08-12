from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import Project
from .models import DataPoints
from .YouTubeClient import YouTubeClient, VideoInfo
from rest_framework.decorators import api_view
from rest_framework.response import Response


def user_login(request):
    if request.user.is_authenticated:
        return redirect("base:home")
    return render(request, 'base/user_login.html')

def how(request):
    return render(request, 'base/howItWorks.html')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        project = Project.objects.filter(customer=customer)
    else:
        return redirect("base:user_login")
    return render(request, 'base/home.html',{"projects":project})
    

def project(request):
    proj = []
    if request.method == 'POST':
        pro_name = request.POST.get('textfield', None)
        if(pro_name != ""):
            customer = request.user
            proj = Project(customer=customer,project_name=pro_name)
            proj.save()
            print(proj)
            return render(request, 'base/project.html', {"projects": proj})
        else:
            print("you must name a project")
            return redirect('/home')

def project2(request,pk):
    proj = Project.objects.get(id=pk)

    Data = DataPoints.objects.filter(project=proj)

    m = []
    y1 = []
    y2 = []

    for i in range(len(Data)):
        m.append(Data[i].month)
        y1.append(Data[i].y1)
        y2.append(Data[i].y2)
        
    print("retreived y1: ",y1)
    print("retreived y2: ",y2)
    y3 = [x for _,x in sorted(zip(m,y1))]
    
    y4 = [x for _,x in sorted(zip(m,y2))]
    

    print("sorted y3: ", y3)
    print("sorted y4: ",y4)

    m = sorted(m)
    print("sorted m: ",m)

    return render(request, 'base/project.html',{"projects": proj,"labels":m,"y1":y3, "y2":y4})

def search(request,pk):
    proj = Project.objects.get(id=pk)
    search = ''
    if request.method == 'POST':
        search = request.POST.get('textfield', None)
        print(search)

    yt = YouTubeClient(search)
    
    proj.search_term = search
    proj.total_views = yt.views
    proj.fav_titles = yt.positive
    proj.unfav_titles = 50-yt.positive
    proj.likes_fav = yt.fav_likes
    proj.dislikes_fav = yt.fav_dislikes
    proj.likes_unfav = yt.unfav_likes
    proj.dislikes_unfav = yt.unfav_dislikes
    proj.total_favourability = ((yt.fav_likes+yt.unfav_dislikes)/(yt.fav_likes+yt.unfav_dislikes+yt.fav_dislikes+yt.unfav_likes))*100
    print(proj.total_favourability)
    proj.save()
    Data = DataPoints.objects.filter(project=proj)
    for i in range(len(Data)):
        Data[i].delete()
        
    print(yt.mlist)
    for i in range(len(yt.mlist)):
        data = DataPoints(project=proj,month=yt.mlist[i],y1=yt.y1[i],y2=yt.y2[i])
        data.save()
    print("from search: ",yt.mlist)
    print("from search: ",yt.y1)
    print("from search: ",yt.y2)

    return render(request, 'base/project.html',{"projects": proj,"labels":yt.mlist,"y1":yt.y1, "y2":yt.y2})
    

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
    pro = Project.objects.get(id=pk)
    pro.delete()
    return  redirect('/home')

