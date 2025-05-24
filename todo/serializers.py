from rest_framework import serializers
from todo.models import Todo, TodoStatus, TodoPriority

class TodoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoStatus
        fields = ['id', 'name', 'created_at', 'updated_at']  

class TodoPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoPriority
        fields = ['id', 'name', 'created_at', 'updated_at']  
        
        
class TodoSerializer(serializers.ModelSerializer):
    status = TodoStatusSerializer(read_only=True)
    priority = TodoPrioritySerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=TodoStatus.objects.all(),
        source='status',
        write_only=True,
        required=False
    )
    priority_id = serializers.PrimaryKeyRelatedField(
        queryset=TodoPriority.objects.all(),
        source='priority',
        write_only=True,
        required=False
    )

    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'description', 'image', 'status', 'priority', 'status_id',
            'priority_id', 'due_date', 'created_at', 'updated_at'
        ]        
        