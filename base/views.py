from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.
# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Lets learn JavaScript'},
#     {'id': 3, 'name': 'Lets learn Shell Scripting'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(topic__name__contains = q)
    context = {"rooms": rooms, "topics": topics}
    return render(request, 'base/home.html', context)

def room(request, pk):
    context = {"room": None}
    context["room"] = Room.objects.get(id=pk)
    return render(request, 'base/room.html', context)

def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {'form': form}
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        form.save()
        return redirect('home')
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)