from django.shortcuts import render,redirect
from projects.models import *
from projects.forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.utils import *
from django.contrib import messages
# Create your views here.

def projects(request):
	all_projects,search_query=searchProjects(request)
	custom_range,all_projects,paginator = paginateProjects(request,all_projects,6)
	context = {'projects': all_projects,'search_query':search_query,'paginator':paginator,'custom_range':custom_range}
	return render(request,"projects/projects.html",context)	

def project(request,pk):
	projectObj = Project.objects.get(id=pk)	
	form = ReviewForm()
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		review = form.save(commit=False)
		review.project = projectObj
		review.owner = request.user.profile
		review.save()
		projectObj.getVoteCount
		messages.success(request,'Review added successfully')
		return redirect('project',pk=projectObj.id)

	context = {'project': projectObj, 'form': form}
	return render(request,"projects/project.html",context)

@login_required(login_url='login')
def create_project(request):
	profile = request.user.profile
	form = ProjectForm()
	if request.method == 'POST':
		form = ProjectForm(request.POST,request.FILES)
		if form.is_valid():
			project = form.save(commit=False)
			project.owner = profile
			project.save()
			return redirect("account")
	context = {'form': form}
	return render(request,"projects/project_form.html",context)

@login_required(login_url='login')
def update_project(request,pk):
	profile = request.user.profile
	project = profile.project_set.get(id=pk)
	form = ProjectForm(instance=project)
	if request.method == 'POST':
		form = ProjectForm(request.POST,request.FILES,instance = project)
		if form.is_valid():
			form.save()
			return redirect("account")
	context = {'form': form}
	return render(request,"projects/project_form.html",context)

@login_required(login_url='login')
def delete_project(request,pk):
	profile = request.user.profile
	project = profile.project_set.get(id=pk)
	if request.method == 'POST':
		project.delete()
		return redirect("projects")
	return render(request,"delete.html",{'project':project})

 

