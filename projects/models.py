from django.db import models
import uuid
from users.models import *
# Create your models here.
class Project(models.Model):
	owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
	title = models.CharField(max_length=150)
	desc = models.TextField(null=True,blank=True)
	demo_link = models.CharField(null=True,blank=True,max_length=2000)
	source_link = models.CharField(null=True,blank=True,max_length=2000)
	featured_image = models.ImageField(null=True,blank=True,default="default.jpg")
	tags = models.ManyToManyField('Tag',blank=True)
	vote_total = models.IntegerField(default=0,null=True,blank=True)
	vote_ratio = models.IntegerField(default=0,null=True,blank=True)
	created = models.DateTimeField(auto_now_add = True)
	id = models.UUIDField(default = uuid.uuid4,primary_key=True,unique=True,editable=False)

	def __str__(self):
	 return self.title

	class Meta:
		ordering = ['-vote_ratio','-vote_total','-title']

	@property
	def reviewers(self):
		queryset = self.review_set.all().values_list('owner__id',flat=True)
		return queryset

	@property
	def getVoteCount(self):
		reviews = self.review_set.all()		
		upvotes = reviews.filter(value='up').count()
		total_votes = reviews.count()
		ratio = (upvotes/total_votes) * 100
		self.vote_total = total_votes 
		self.vote_ratio = ratio
		self.save()

	class Meta:
		ordering = ['-created']

class Review(models.Model):
	VOTE_TYPE = (
		('up','Up Vote'),
		('down','Down Vote')
	)
	owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
	project = models.ForeignKey(Project,on_delete=models.CASCADE) # Getting projects from project table
	body = models.TextField(null=True,blank=True)
	value = models.CharField(max_length=200,choices=VOTE_TYPE)
	created = models.DateTimeField(auto_now_add = True)
	id = models.UUIDField(default = uuid.uuid4,primary_key=True,unique=True,editable=False)

	class Meta:
		unique_together = [['owner','project']] # Both should be unique i.e a project should have only one comment

	def __str__(self):
	 return self.value

	
class Tag(models.Model):
	name = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add = True)
	id = models.UUIDField(default = uuid.uuid4,primary_key=True,unique=True,editable=False)

	def __str__(self):
	 return self.name


#  Project is ONE TO MANY RELATIONSHIP to Tag table