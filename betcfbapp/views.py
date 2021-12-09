from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Widget
from .forms import CreateNewList

# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for widget in ls.widget_set.all():
                if response.POST.get("c" + str(widget.id)) == "clicked":
                    widget.complete = True
                else:
                    widget.complete = False
                widget.save()
        
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2 :
                ls.widget_set.create(text=txt, complete=False)
            else:
                print("Invalid input")
    
    return render(response, "betcfbapp/list.html", {"ls":ls})

def home(response):
    return render(response, "betcfbapp/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()

    return render(response, "betcfbapp/create.html", {"form":form})

def view(response):
    return render(response, "betcfbapp/view.html", {})