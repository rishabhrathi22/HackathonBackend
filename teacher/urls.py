from django.urls import include, path
from rest_framework import routers

from . import views

teacher_view = views.TeacherViewSet.as_view({'get':'list'})
teacher_create = views.TeacherViewSet.as_view({'post':'create'})
teacher_login = views.TeacherViewSet.as_view({'post':'login'})

urlpatterns = [
	
	path('', teacher_view),
	path('register/', teacher_create),
	path('login/', teacher_login),
]
