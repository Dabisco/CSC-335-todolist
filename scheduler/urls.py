from django.urls import path
from scheduler import views

urlpatterns = [
    path('events/', views.event_list_create_view, name='event-list-create'),
    path('events/<int:pk>/', views.event_detail_view, name='event-detail'),
]
