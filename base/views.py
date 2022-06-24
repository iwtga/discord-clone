from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


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
    topics = Topic.objects.all()[:5]
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q) |
                                Q(host__username__icontains=q))
    rmsgs = Message.objects.filter(Q(body__icontains=q) |
                                   Q(room__name__icontains=q) |
                                   Q(room__topic__name__icontains=q))
    context = {"rooms": rooms, "topics": topics,
               "room_count": rooms.count(), 'rmsgs': rmsgs}
    return render(request, 'base/home.html', context)


def profile_page(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    rmsgs = user.message_set.all()
    context = {'user': user, "topics": topics, "rooms": rooms, "rmsgs": rmsgs}
    return render(request, 'base/profile.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    rmsgs = room.message_set.all().order_by('-updated')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'base/room.html', {'room': room, 'rmsgs': rmsgs, 'participants': participants})


@login_required(login_url='login')
def create_room(request):
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')
    form = RoomForm()
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not authorized to perform the action!")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
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

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile-page', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activity_page(request):
    rmsgs = Message.objects.all()
    return render(request, 'base/activity.html', {'rmsgs': rmsgs})