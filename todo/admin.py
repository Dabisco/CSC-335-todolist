from django.contrib import admin
from . models import TodoStatus, TodoPriority, Todo
# Register your models here.

admin.site.register(TodoStatus)
admin.site.register(TodoPriority)
admin.site.register(Todo)
