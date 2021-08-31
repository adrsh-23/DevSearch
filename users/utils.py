from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import * 

def searchProfiles(request):
	search_query = ''
	if request.GET.get('search_query'):
		search_query = request.GET.get('search_query')

	skills = Skill.objects.filter(name__iexact=search_query)
	profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query)|Q(skill__in=skills))
	return profiles,search_query


def paginateProfiles(request,profiles,results):
	
	page = request.GET.get('page') 

	paginator = Paginator(profiles,results)

	try:
		profiles = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		profiles = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
		profiles = paginator.page(page)

	left_index = (int(page)-1)

	if left_index < 1:
		left_index = 1
	right_index = (int(page)+1)
	if right_index > paginator.num_pages:
		right_index = paginator.num_pages + 1
	
	custom_range = range(left_index,right_index+1)

	return custom_range,profiles
