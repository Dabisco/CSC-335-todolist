from django.urls import path
from todo import views

urlpatterns = [
    # Status
    path('status/', views.todo_status_list_create, name='todo-status-list-create'),
    path('status/<int:pk>/', views.todo_status_detail_update_delete, name='todo-status-detail'),

    # Priority
    path('priority/', views.todo_priority_list_create, name='todo-priority-list-create'),
    path('priority/<int:pk>/', views.todo_priority_detail_update_delete, name='todo-priority-detail'),
    
    #Todo
    path('todos/', views.todo_list_create, name='todo-list-create'),
    path('todos/<int:pk>/', views.todo_detail_update_delete, name='todo-detail'),
]
