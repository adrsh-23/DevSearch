from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from users.models import * 
from users.forms import *
from users.utils import *
# Create your views here.

def login_page(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		username = request.POST['username'].lower()
		password = request.POST['password']
		try: 
			user = User.objects.get(username=username)
		except:
			messages.error(request,'Username does not exist')
		
		user = authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			return redirect(request.GET['next'] if 'next' in request.GET else 'account')
		else:
			messages.error(request,'Username/Password is incorrect')

	return render(request,"users/login.html")

def register_user(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			messages.success(request,'User created')
			login(request,user)
			return redirect('edit-account')
		else:
			messages.error(request,'An error has occurred during registration')

	context = {'form':form}
	return render(request,'users/register.html',context)

def logout_user(request):
	logout(request)
	messages.info(request,'User was logged out successfully')
	return redirect('login')

def profiles(request):
	profiles,search_query = searchProfiles(request)	

	custom_range,profiles = paginateProfiles(request,profiles,3)

	context = {'users':profiles,'search_query':search_query,'custom_range':custom_range}
	return render(request,'users/profiles.html',context)

def user_profile(request,pk):
	user = Profile.objects.get(id=pk)
	skills = user.skill_set.exclude(desc__exact="")
	other_skills = user.skill_set.filter(desc="")
	context = {'user':user,'skills':skills,'other_skills':other_skills}
	return render(request,'users/user_profile.html',context)


@login_required(login_url="login")
def userAccount(request):
	profile = request.user.profile
	skills = profile.skill_set.all()
	projects = profile.project_set.all()
	context = {'profile':profile,'skills':skills,'projects':projects}
	return render(request,'users/user_account.html',context)

@login_required(login_url='login')
def editAccount(request):
	profile = request.user.profile
	form = ProfileForm(instance=profile)
	if request.method == 'POST':
		form = ProfileForm(request.POST,request.FILES,instance=profile)
		if form.is_valid():
			form.save()
			return redirect('account')
	context = {'form':form}
	return render(request,'users/profile_form.html',context)


@login_required(login_url='login')
def create_skill(request):
	profile = request.user.profile
	form = SkillForm()
	if request.method == 'POST':
		form = SkillForm(request.POST)
		if form.is_valid():
			skill = form.save(commit=False)
			skill.owner = profile
			skill.save()
			messages.success(request,'Skill was added successfully!')
			return redirect('account')
	context = {'form':form}
	return render(request,"users/skill_form.html",context)


@login_required(login_url='login')
def update_skill(request,pk):
	profile = request.user.profile
	skill = profile.skill_set.get(id=pk)
	form = SkillForm(instance=skill)
	if request.method == 'POST':
		form = SkillForm(request.POST,instance=skill)
		if form.is_valid():
			form.save()
			messages.success(request,'Skill was updated successfully!')
			return redirect('account')
	context = {'form':form}
	return render(request,"users/skill_form.html",context)

@login_required(login_url='login')
def delete_skill(request,pk):
	profile = request.user.profile
	skill = profile.skill_set.get(id=pk)
	if request.method == 'POST':
		skill.delete()
		messages.success(request,'Skill was deleted successfully!')
		return redirect('account')
	context = {'object':skill}
	return render(request,"delete.html",context)


@login_required(login_url='login')
def inbox(request):
	profile = request.user.profile
	msg = profile.messages.all()
	unread_count = msg.filter(is_read=False).count()
	context = {'msg':msg,'unread_count':unread_count}
	return render(request,'users/inbox.html',context)


@login_required(login_url='login')
def view_message(request,pk):
	msg = Message.objects.get(id=pk)
	msg.msg_read
	context = {'msg':msg}
	return render(request,'users/message.html',context)

def send_message(request,pk):
	form = MessageForm()
	recipient = Profile.objects.get(id=pk)
	try:
		sender = request.user.profile
	except:
		sender = None 
	
	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.sender = sender 
			message.recipient = recipient
			if sender:
				message.name = sender.name	
				message.email = sender.email

			message.save()
			messages.success(request,"Message sent successfully!")
			return redirect('user_profile',pk=recipient.id)
	context = {'form':form,'recipient':recipient}
	return render(request,'users/message_form.html',context)