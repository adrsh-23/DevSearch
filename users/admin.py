from django.contrib import admin

# Register your models here.
from users.models import *

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)
