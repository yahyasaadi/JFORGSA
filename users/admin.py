from django.contrib import admin
from .models import Profile, Vote, ProfileAdmin, VoteAdmin

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Vote, VoteAdmin)