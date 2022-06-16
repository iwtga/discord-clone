from email import message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


def login_page(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        except:
            messages.error(request, 'Username not found')

    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(topic__name__icontains = q) |
                                Q(name__icontains = q) |
                                Q(description__icontains = q) |
                                Q(host__username__icontains = q))
    context = {"rooms": rooms, "topics": topics, "room_count": rooms.count()}
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