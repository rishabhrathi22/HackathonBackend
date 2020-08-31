from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
	openapi.Info(
		title="Snippets API",
		default_version='v1',
		description="Test description",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="contact@snippets.local"),
		license=openapi.License(name="BSD License"),
		),
	public=True,
	permission_classes=(permissions.AllowAny,),
	)


urlpatterns = [
	url('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('', views.opendocs, name="opendocs"),
	path('institution/', include('institution.urls')),
	path('teacher/', include('teacher.urls')),
	path('student/', include('student.urls')),
	path('classroom/', include('classroom.urls')),
	path('superuser/', include('users.urls')),
	path('admin/', admin.site.urls),
]
