from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.
STREAMS = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')]
AGENT_ROLE = [('pollingAgent', 'Polling Agent'), ('chiefAgent', 'Chief Agent')]
WARDS = [('galbet','GALBET'),('waberi','WABERI'),('iftin','IFTIN'),('township','TOWNSHIP')]
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ward = models.CharField(max_length=50,choices=WARDS)
    pollingStation = models.CharField(max_length=50)
    stream = models.CharField( max_length=50, choices=STREAMS)
    phone = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    role = models.CharField(max_length=50,choices=AGENT_ROLE, default='Polling Agent')
    
    
    def __str__(self):
        return self.fullname + ' - ' + self.pollingStation
    
    

class Vote(models.Model):
    sender_username = models.CharField(max_length=100)
    pollingStation = models.CharField(max_length=200)
    ward = models.CharField(max_length=200)
    stream = models.CharField(max_length=50)
    registerdVoters = models.IntegerField()
    rejected = models.IntegerField()
    rejectedObj = models.IntegerField()
    disputed = models.IntegerField()
    valid = models.IntegerField()
    jofle = models.IntegerField()
    osman = models.IntegerField()
    major = models.IntegerField()
    feisal = models.IntegerField()
    malow = models.IntegerField()
    muhiadin = models.IntegerField()
    
    def __str__(self) -> str:
        return self.pollingStation + ' -- ' + self.ward
    
    

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['id_number', 'fullname', 'pollingStation','phone']
    

class VoteAdmin(admin.ModelAdmin):
    search_fields = ['pollingStation', 'ward']