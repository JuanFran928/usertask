from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task

# Create your views here. Pasar todas las vistas a APIVIEW

@api_view(['GET'])
def apiOverview(request):
    
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create':'/task-create/',
        'Update': '/task-update/',
        'Delete':'/task-delete/<str:pk>/'
    }
    
    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
    if request.user.is_authenticated:
        queryset = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
    raise AuthenticationFailed('Unauthenticated!')

@api_view(['GET'])
def taskDetail(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk, user= request.user)
            serializer = TaskSerializer(task, many= False)
        except Task.DoesNotExist:
            return Response(
                    {'status': 'Task not found'},
                    status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
    raise AuthenticationFailed('Unauthenticated!')

@api_view(['POST'])
def create_task(request):
    if request.user.is_authenticated:
        serializer = TaskSerializer(data = request.data)
        request.data['user'] = request.user.id
        
        if serializer.is_valid():
            serializer.save()
            
        return Response(serializer.data)
    raise AuthenticationFailed('Unauthenticated!')

@api_view(['PUT'])
def update_task(request, pk):
    if request.user.is_authenticated: 
        try:
            task = Task.objects.get(id=pk, user= request.user)
            serializer = TaskSerializer(instance=task, data = request.data)
            request.data['user'] = request.user.id
        except Task.DoesNotExist:
            return Response(
                    {'status': 'Task not found'},
                    status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    raise AuthenticationFailed('Unauthenticated!')

@api_view(['DELETE'])
def delete_task(request, pk):
    if request.user.is_authenticated: 
        try:
            print(pk)
            Task.objects.filter(id=pk, user=request.user).delete()
        except Task.DoesNotExist:
            return Response(
                    {'status': 'Task not found'},
                    status=status.HTTP_404_NOT_FOUND)
        
        return Response("Eliminado correctamente")
    raise AuthenticationFailed('Unauthenticated!')