from django.contrib import admin
from .models import Profile, Vote, ProfileAdmin, VoteAdmin,Preliminary,PreliminaryAdmin

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Preliminary,PreliminaryAdmin)