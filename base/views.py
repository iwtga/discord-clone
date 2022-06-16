from django.shortcuts import render
from .models import Room

# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Lets learn JavaScript'},
#     {'id': 3, 'name': 'Lets learn Shell Scripting'},
# ]

def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    context = {"room": None}
    context["room"] = Room.objects.get(id=pk)
    return render(request, 'base/room.html', context)