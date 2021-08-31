from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from projects.models import * 

def searchProjects(request):
	search_query = ''
	if request.GET.get('search_query'):
		search_query = request.GET.get('search_query')
	tags = Tag.objects.filter(name__icontains=search_query)
	all_projects = Project.objects.distinct().filter(Q(title__icontains=search_query)|Q(owner__name__icontains=search_query) | Q(tags__in=tags))
	return all_projects,search_query


def paginateProjects(request,all_projects,results):

	page = request.GET.get('page') 
	results = 3 

	paginator = Paginator(all_projects,results)

	try:
		all_projects = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		all_projects = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
		all_projects = paginator.page(page)

	left_index = (int(page)-1)

	if left_index < 1:
		left_index = 1
	right_index = (int(page)+1)
	if right_index > paginator.num_pages:
		right_index = paginator.num_pages + 1
	
	custom_range = range(left_index,right_index+1)

	return custom_range,all_projects,paginator
