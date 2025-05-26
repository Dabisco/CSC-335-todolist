from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import TodoStatus, TodoPriority, Todo
from .serializers import TodoStatusSerializer, TodoPrioritySerializer, TodoSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status as http_status


# === TodoStatus ===
@swagger_auto_schema(method='post', request_body=TodoStatusSerializer, responses={201: TodoStatusSerializer})
@swagger_auto_schema(method='get', responses={200: TodoStatusSerializer(many=True)})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todo_status_list_create(request):
    if request.method == 'GET':
        queryset = TodoStatus.objects.all()
        serializer = TodoStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.data.get('name')
        if TodoStatus.objects.filter(name__iexact=name).exists():
            return Response({'detail': 'Status already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TodoStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@swagger_auto_schema(method='get', responses={200: TodoStatusSerializer})
@swagger_auto_schema(method='put', request_body=TodoStatusSerializer, responses={200: TodoStatusSerializer})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_status_detail_update_delete(request, pk):
    status_obj = get_object_or_404(TodoStatus, pk=pk)

    if request.method == 'GET':
        serializer = TodoStatusSerializer(status_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoStatusSerializer(status_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        status_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# === TodoPriority ===
@swagger_auto_schema(method='post', request_body=TodoPrioritySerializer, responses={201: TodoPrioritySerializer})
@swagger_auto_schema(method='get', responses={200: TodoPrioritySerializer(many=True)})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todo_priority_list_create(request):
    if request.method == 'GET':
        queryset = TodoPriority.objects.all()
        serializer = TodoPrioritySerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.data.get('name')
        if TodoPriority.objects.filter(name__iexact=name).exists():
            return Response({'detail': 'Priority already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TodoPrioritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='get', responses={200: TodoPrioritySerializer})
@swagger_auto_schema(method='put', request_body=TodoPrioritySerializer, responses={200: TodoPrioritySerializer})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_priority_detail_update_delete(request, pk):
    priority_obj = get_object_or_404(TodoPriority, pk=pk)

    if request.method == 'GET':
        serializer = TodoPrioritySerializer(priority_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoPrioritySerializer(priority_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        priority_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# === TodoList ===

@swagger_auto_schema(method='get', responses={200: TodoSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=TodoSerializer, responses={201: TodoSerializer})
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todo_list_create(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: TodoSerializer})
@swagger_auto_schema(method='put', request_body=TodoSerializer, responses={200: TodoSerializer})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_detail_update_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)