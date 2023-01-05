from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegisterForm, ProfileUpdateForm, VoteForm
from .models import Profile, Vote,Preliminary
import pyrebase
import time
import datetime

# Create your views here.




@login_required
def home(request):
    # name = Profile.objects.get(id=request.user.id)
    user = request.user
    name = Profile.objects.get(user=user)
    vote = Vote.objects.filter(sender_username=request.user.username)
    if vote:
        return render(request,'users/submitted.html',{'vote':vote})
    else:
        if request.method == 'POST':
            ward = request.POST['ward']
            sender_username = request.POST['sender_username']
            pollingStation = request.POST['pollingStation']
            stream = request.POST['stream']
            registerdVoters = request.POST['registerdVoters']
            rejected = request.POST['rejected']
            rejectedObj = request.POST['rejectedObj']
            disputed = request.POST['disputed']
            valid = request.POST['valid']
            jofle = request.POST['jofle']
            dekow = request.POST['dekow']
            osman = request.POST['osman']
            feisal = request.POST['feisal']
            malow = request.POST['malow']
            # muhiadin = request.POST['muhiadin']
            # print(ward, pollingStation, valid, osman)
            # print(f'sender_username: {sender_username}')
            new_vote = Vote(sender_username=sender_username,ward=ward, pollingStation=pollingStation,stream=stream, registerdVoters=registerdVoters, rejected=rejected,
                            rejectedObj=rejectedObj, disputed=disputed, valid=valid, jofle=jofle, major=dekow, osman=osman,feisal=feisal,muhiadin=0,malow=malow)
            new_vote.save()
            firebaseConfig = {
                'apiKey': "AIzaSyCqMdmrITPM8x4PdMqP5T9Hcmmj5IJPH6M",
                'authDomain': "demoapp-607db.firebaseapp.com",
                'databaseURL': "https://demoapp-607db-default-rtdb.asia-southeast1.firebasedatabase.app",
                'projectId': "demoapp-607db",
                'storageBucket': "demoapp-607db.appspot.com",
                'messagingSenderId': "641799333572",
                'appId': "1:641799333572:web:fd402ab5271f9fa4d6cb91",
                'measurementId': "G-KPVXQKZ7KK"
                # "serviceAccount":"serviceAccount.json"
                }
            firebase = pyrebase.initialize_app(firebaseConfig)
            
            db = firebase.database()
            
            data = {
                'time':time.ctime(),
                'ward': ward,
                'pollingStation': (pollingStation+stream),
                'registerdVoters': registerdVoters,
                'rejected': rejected,
                'rejectedObj': rejectedObj,
                'disputed': disputed,
                'valid': valid, 
                'jofle': jofle,
                'dekow': dekow, 
                'osman': osman,
                'malow': malow,
                'feisal': feisal,
                'muhiadin': 0
            }
            
            if name.role == 'pollingAgent':
                result = db.child('votes').child(pollingStation+stream).set(data)
            else:
                result = db.child('chiefAgents').child(pollingStation+stream).set(data)
                
            # result = firebase.database().ref(f"votes/{pollingStation}").setValue(data)

            # print(result)
            return render(request, 'users/confirm_votes.html',{'name':name})
        else:
            return render(request, 'users/home.html', {'name':name})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! Login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        # user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # if user_update_form.is_valid() and profile_update_form.is_valid():
        if profile_update_form.is_valid():
            # user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
    else:
        # user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        # 'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }
    return render(request, 'users/update.html', context)



@login_required
def preliminary(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    return render(request, 'users/preliminary.html',{'profile':profile})

def sendPreliminary (request):
    if request.method == 'POST':
        ward = request.POST['ward']
        pollingStation = request.POST['pollingStation']
        stream = request.POST['stream']
        fullname = request.POST['fullname']
        osman = request.POST['osman']
        dolal = request.POST['dolal']
        dekow = request.POST['dekow']
        malow = request.POST['malow']
        feisal = request.POST['feisal']
        new_preliminary = Preliminary(pollingStation=pollingStation,time=time.ctime(),ward=ward,stream=stream,fullname=fullname,osman=osman,dolal=dolal,dekow=dekow,malow=malow,feisal=feisal)
        new_preliminary.save()
        messages.success(request, f'You have sent your preliminary result at: {time.ctime()}')
        return redirect('home')
    else:
        return redirect('preliminary')


def panel(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if ((username=='Jofle2023admin') and password=='Jofle4GSA2023'):
            preliminary= Preliminary.objects.all()
            return render(request, 'users/panel.html',{'preliminary':preliminary})
        else:
            return render(request,'users/login1.html')
    else:
        return render(request,'users/login1.html')
    
    