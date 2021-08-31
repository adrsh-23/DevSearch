from django.urls import path
from . import views
urlpatterns = [
	path('login/',views.login_page,name="login"),
	path('register/',views.register_user,name="register"),
	path('logout/',views.logout_user,name="logout"),
	path('',views.profiles,name='profiles'),
	path('profile/<str:pk>/',views.user_profile,name='user_profile'),
	path('account/',views.userAccount,name="account"),
	path('edit-account/',views.editAccount,name="edit-account"),
	path('create-skill/',views.create_skill,name="create-skill"),
	path('update-skill/<str:pk>/',views.update_skill,name="update-skill"),
	path('delete-skill/<str:pk>/',views.delete_skill,name="delete-skill"),
	path('inbox/',views.inbox,name="inbox"),
	path('message/<str:pk>/',views.view_message,name="message"),
	path('send_message/<str:pk>/',views.send_message,name="send_message"),
]
