from django.shortcuts import render

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Lets learn Python'},
    {'id': 2, 'name': 'Lets learn JavaScript'},
    {'id': 3, 'name': 'Lets learn Shell Scripting'},
]

def home(request):
    context = {"rooms": rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    context = {"room": None}
    for i in rooms:
        if i['id'] == int(pk):
            context["room"] = i
    return render(request, 'base/room.html', context)