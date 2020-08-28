from django.urls import include, path
from rest_framework import routers

from . import views

inst_view = views.InstituteViewSet.as_view({'get':'list'})
inst_create = views.InstituteViewSet.as_view({'post':'create'})
inst_login = views.InstituteViewSet.as_view({'post':'login'})

# router = routers.DefaultRouter()
# router.register(r'', views.InstituteViewSet, basename='institute')

urlpatterns = [
	path('', inst_view),
	path('register/', inst_create),
	path('login/', inst_login),
]
