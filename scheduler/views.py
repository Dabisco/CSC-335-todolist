from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ScheduledEvent
from .serializers import ScheduledEventSerializer

@swagger_auto_schema(
    method='get',
    responses={200: ScheduledEventSerializer(many=True)},
    operation_summary="List all scheduled events"
)
@swagger_auto_schema(
    method='post',
    request_body=ScheduledEventSerializer,
    responses={201: ScheduledEventSerializer},
    operation_summary="Create a new scheduled event"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list_create_view(request):
    if request.method == 'GET':
        events = ScheduledEvent.objects.filter(user=request.user).order_by('-start_datetime')
        serializer = ScheduledEventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScheduledEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: ScheduledEventSerializer},
    operation_summary="Retrieve a scheduled event"
)
@swagger_auto_schema(
    method='put',
    request_body=ScheduledEventSerializer,
    responses={200: ScheduledEventSerializer},
    operation_summary="Update a scheduled event (partial)"
)
@swagger_auto_schema(
    method='delete',
    responses={204: 'Deleted'},
    operation_summary="Delete a scheduled event"
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail_view(request, pk):
    try:
        event = ScheduledEvent.objects.get(pk=pk, user=request.user)
    except ScheduledEvent.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ScheduledEventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ScheduledEventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)