from django.db import models
from account.models import User
from django.utils import timezone
# Create your models here.

class TodoStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_statuses')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TodoPriority(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_priorities')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='todo_images/', blank=True, null=True)
    status = models.ForeignKey(TodoStatus, on_delete=models.CASCADE, related_name='todos', blank=True, null=True)
    priority = models.ForeignKey(TodoPriority, on_delete=models.CASCADE, related_name='todos', blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Todos'
    
    def __str__(self):
        return self.title
    
