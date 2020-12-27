from django.urls import include, path
from rest_framework import routers

from . import views

student_create = views.StudentViewSet.as_view({'post':'create'})
student_login = views.StudentViewSet.as_view({'post':'login'})
student_logout = views.StudentViewSet.as_view({'post':'logout'})
student_detail = views.StudentViewSet.as_view({'post': 'retrieve'})
student_change_pwd = views.StudentViewSet.as_view({'post':'change_password'})
student_send_message = views.StudentViewSet.as_view({'post': 'chat_with_teacher'})

urlpatterns = [

	path('', student_detail),
	path('register/', student_create),
	path('login/', student_login),
	path('logout/', student_logout),
	path('<str:name>/change-password', student_change_pwd),
	path('chat/', student_send_message),
	# path('<str:name>/', student_detail)
]
