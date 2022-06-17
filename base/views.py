from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm


def login_page(request):
    context = {'form_page': 'login'}

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username").lower()
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


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error occured during registration")

    return render(request, 'base/login_register.html', {'form': form})


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
    room = Room.objects.get(id=pk)
    rmsgs = room.message_set.all().order_by('-updated')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'base/room.html', {'room': room, 'rmsgs': rmsgs, 'participants': participants})

@login_required(login_url='login')
def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not authorized to perform the action!")

    context = {'form': form}
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        form.save()
        return redirect('home')
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}
    if request.user != room.host:
        return HttpResponse("You are not authorized to perform the action!")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not authorized to perform the action!")
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})