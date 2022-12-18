from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.
AGENT_ROLE = [('pollingAgent', 'Polling Agent'), ('chiefAgent', 'Chief Agent')]
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    ward = models.CharField(max_length=50)
    pollingStation = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    role = models.CharField(max_length=50,choices=AGENT_ROLE, default='Polling Agent')
    
    
    def __str__(self):
        return self.fullname + ' - ' + self.pollingStation
    
    

class Vote(models.Model):
    pollingStation = models.CharField(max_length=200)
    ward = models.CharField(max_length=200)
    registerdVoters = models.IntegerField()
    rejected = models.IntegerField()
    rejectedObj = models.IntegerField()
    disputed = models.IntegerField()
    valid = models.IntegerField()
    jofle = models.IntegerField()
    osman = models.IntegerField()
    major = models.IntegerField()
    suleiman = models.IntegerField()
    
    def __str__(self) -> str:
        return self.pollingStation + ' -- ' + self.ward
    
    

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['id_number', 'fullname', 'pollingStation','phone']
    

class VoteAdmin(admin.ModelAdmin):
    search_fields = ['pollingStation', 'ward']