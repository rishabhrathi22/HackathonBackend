from django.urls import include, path
from rest_framework import routers

from . import views

class_view = views.ClassroomViewSet.as_view({'get':'list'})
class_create = views.ClassroomViewSet.as_view({'post':'create'})
class_detail = views.ClassroomViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
	
	path('', class_view),
	path('create/', class_create),
	path('<str:standard>/<str:section>/<str:subject>/', class_detail)
]
