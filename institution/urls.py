from django.urls import include, path
from rest_framework import routers

from . import views

# inst_view = views.InstituteViewSet.as_view({'get':'list'})
inst_detail = views.InstituteViewSet.as_view({'post': 'retrieve'})
inst_create = views.InstituteViewSet.as_view({'post':'create'})
inst_login = views.InstituteViewSet.as_view({'post':'login'})
inst_logout = views.InstituteViewSet.as_view({'post':'logout'})
inst_change_pwd = views.InstituteViewSet.as_view({'post':'change_password'})
inst_approve_teacher = views.InstituteViewSet.as_view({'post':'approveTeacher'})
inst_get_all_teachers = views.InstituteViewSet.as_view({'post': 'getAllTeachers'})


urlpatterns = [
	path('', inst_detail),
	path('register/', inst_create),
	path('login/', inst_login),
	path('logout/', inst_logout),
	path('<str:name>/change-password', inst_change_pwd),
	path('approve-teacher/', inst_approve_teacher),
	path('allteachers', inst_get_all_teachers),
]
