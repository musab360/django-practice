from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from myproject.settings import require_jwt
from django.http import HttpResponse, JsonResponse
from .models import TaskCreation, TaskUpdated

# Create your views here.
@csrf_exempt
@require_jwt
def task_creation(request):
    user = request.jwt_user  # Access decoded JWT payload
    request_data = json.loads(request.body)
    TaskCreation.objects.create(
        created_by_id=user.get("user_id"),
        title=request_data.get("title"),
        description=request_data.get("description")
    )
    return JsonResponse({"response": "Task created successfully!"})

@require_jwt
@csrf_exempt
def task_retrieval(request):
    user = request.jwt_user  # Access decoded JWT payload
    tasks = TaskCreation.objects.filter(created_by_id=user.get("user_id"))
    print(tasks)
    return JsonResponse({"tasks": tasks})

@csrf_exempt
@require_jwt
def task_retrieval(request):
    user = request.jwt_user  # Access decoded JWT payload
    return JsonResponse({"user": user})