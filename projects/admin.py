from django.contrib import admin
from projects.models import * 
# Register your models here.
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Review)