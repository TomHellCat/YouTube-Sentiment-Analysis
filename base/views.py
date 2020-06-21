from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import Project
#from .youtubeClient import YoutubeClient
from .newClient import YoutubeClient, VideoInfo
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
    
    m = proj.months
    y1 = proj.y1
    y2 = proj.y2
    return render(request, 'base/project.html',{"projects": proj,"labels":m,"y1":y1, "y2":y2})

def search(request,pk):
    proj = Project.objects.get(id=pk)
    search = ''
    if request.method == 'POST':
        search = request.POST.get('textfield', None)
        print(search)

    yt = YoutubeClient(search)
    yt.create_video_info_objects()
    format = "%d %b %Y"
    months = yt.get_months()
    print(len(months))
    m = yt.monthlist_fast(months[0],months[len(months)-1])
    for i in months:
        print(i.strftime(format))
    print(m)
    y = yt.get_y_axis(m,months)
    print(y)
    fav,unfav = yt.get_total_fav_unfav()
    print("fav: ",fav, " unfav: ",unfav)
    
    print("views: ", yt.get_total_views())
    lfav,lunfav = yt.total_likes_fav_unfav()

    print("likes for fav: ",lfav," likes for unfav: ", lunfav)

    dfav, dunfav = yt.total_dislikes_fav_unfav()

    print("dislikes for fav: ",dfav," dislikes for unfav: ", dunfav)
    t_fav = lfav + dunfav
    t_unfav = lunfav + dfav
    t_fav = round(t_fav/(t_fav+t_unfav)*100)
    print("t_fav: ", t_fav, " t_unfav: ", t_unfav)

    m_fav,m_unfav = yt.fav_unfav_monthlist(months)
    print("m_fav: ")
    for i in m_fav:
        print(i.strftime(format))
    print("m_unfav: ")
    for i in m_unfav:
        print(i.strftime(format))

    y_fav = yt.get_y_axis(m,m_fav)
    print("y_fav: ",y_fav)
    y_unfav = yt.get_y_axis(m,m_unfav)
    print("y_unfav: ", y_unfav)

    new_m = []
    for i in m:
        s = ''
        j = 0
        while(i[j] != " "):
            s += i[j]
            j += 1
        s += "\n"
        j += 1
        for k in range(j,len(i)):
            s += i[k]
        new_m.append(s)

    print(new_m)
    

    proj.search_term = search
    proj.total_views = yt.get_total_views()
    proj.fav_titles = fav
    proj.unfav_titles = unfav
    proj.likes_fav = lfav
    proj.dislikes_fav = dfav
    proj.likes_unfav = lunfav
    proj.dislikes_unfav = dunfav
    proj.total_favourability = t_fav
    proj.months = new_m
    proj.y1 = y_fav
    proj.y2 = y_unfav
    proj.save()
    return render(request, 'base/project.html',{"projects": proj,"labels":new_m,"y1":y_fav, "y2":y_unfav})
    

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

