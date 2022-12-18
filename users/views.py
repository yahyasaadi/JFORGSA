from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, VoteForm
from .models import Profile, Vote
import pyrebase
import time
import datetime

# Create your views here.




@login_required
def home(request):
    name = Profile.objects.get(id=request.user.id)
    if request.method == 'POST':
        ward = request.POST['ward']
        pollingStation = request.POST['pollingStation']
        registerdVoters = request.POST['registerdVoters']
        rejected = request.POST['rejected']
        rejectedObj = request.POST['rejectedObj']
        disputed = request.POST['disputed']
        valid = request.POST['valid']
        jofle = request.POST['jofle']
        dekow = request.POST['dekow']
        osman = request.POST['osman']
        # print(ward, pollingStation, valid, osman)
        new_vote = Vote(ward=ward, pollingStation=pollingStation, registerdVoters=registerdVoters, rejected=rejected,
                        rejectedObj=rejectedObj, disputed=disputed, valid=valid, jofle=jofle, major=dekow, osman=osman,suleiman=0)
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
            'pollingStation': pollingStation,
            'registerdVoters': registerdVoters,
            'rejected': rejected,
            'rejectedObj': rejectedObj,
            'disputed': disputed,
            'valid': valid, 
            'jofle': jofle,
            'dekow': dekow, 
            'osman': osman
        }
        
        if name.role == 'pollingAgent':
            result = db.child('votes').child(pollingStation).set(data)
        else:
            result = db.child('chiefAgents').child(pollingStation).set(data)
            
        # result = firebase.database().ref(f"votes/{pollingStation}").setValue(data)

        print(result)
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