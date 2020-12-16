from django.urls import include, path
from rest_framework import routers

from . import views

chat_view = views.ChatViewSet.as_view({'post': 'chatFunction'})
chat_view_teacher = views.ChatViewSet.as_view({'post': 'chatFunction1'})
chat_filter = views.ChatViewSet.as_view({'get': 'listofchat'})

urlpatterns = [
    path('', chat_view),
    path('teacher/', chat_view_teacher),
    path('<int:classroom_id>/', chat_filter),
]