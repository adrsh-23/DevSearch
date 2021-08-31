from django.db import models
from django.contrib.auth.models import User
import uuid
from projects.models import *

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	name = models.CharField(max_length=200,blank=True,null=True)
	email = models.EmailField(max_length=500,blank=True,null=True)
	username = models.CharField(max_length=200,blank=True,null=True)
	location = models.CharField(max_length=200,blank=True,null=True)
	short_intro = models.CharField(max_length=500,blank=True,null=True)
	bio = models.TextField(blank=True,null=True)
	profile_image = models.ImageField(null=True,blank=True,upload_to='profiles/',default='profiles/user.png')
	social_github = models.CharField(max_length=200,blank=True,null=True)
	social_twitter = models.CharField(max_length=200,blank=True,null=True)
	social_linkedin = models.CharField(max_length=200,blank=True,null=True)
	social_stackoverflow = models.CharField(max_length=200,blank=True,null=True)
	social_website = models.CharField(max_length=200,blank=True,null=True)
	created = models.DateTimeField(auto_now_add = True)
	id = models.UUIDField(default = uuid.uuid4,primary_key=True,unique=True,editable=False)

	def __str__(self):
		return str(self.username)



class Skill(models.Model):
	owner = models.ForeignKey(Profile ,null=True,blank=True,on_delete=models.CASCADE)
	name = models.CharField(max_length=200,blank=True,null=True)
	desc = models.TextField(null=True,blank=True)
	created = models.DateTimeField(auto_now_add = True)
	id = models.UUIDField(default = uuid.uuid4,primary_key=True,unique=True,editable=False)
		
	def __str__(self):
		return str(self.name)

class Message(models.Model):
	sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
	recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="messages")
	name = models.CharField(max_length=200,null=True,blank=True)
	email = models.EmailField(max_length=200,null=True,blank=True)
	subject = models.CharField(max_length=200,null=True,blank=True)
	body = models.TextField()
	is_read = models.BooleanField(default=False,null=True)
	created = models.DateTimeField(auto_now_add = True)
	id = models.UUIDField(default = uuid.uuid4,primary_key=True,unique=True,editable=False)

	def __str__(self):
		return self.subject
	
	class Meta:
		ordering = ['is_read','-created']

	@property
	def msg_read(self):
		self.is_read = True 
		self.save()

	

	