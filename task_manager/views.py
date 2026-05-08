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
    task = TaskCreation.objects.create(
        created_by_id=user.get("user_id"),
        title=request_data.get("title"),
        description=request_data.get("description")
    )
    return JsonResponse({"response": "Task created successfully!", "id": task.id})

@csrf_exempt
@require_jwt
def task_retrieval(request):
    user = request.jwt_user  # Access decoded JWT payload
    tasks = TaskCreation.objects.filter(
        created_by_id=user.get("user_id")
    )
    tasks_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        for task in tasks
    ]
    return JsonResponse({"tasks": tasks_list})

@csrf_exempt
@require_jwt
def task_update(request):
    user = request.jwt_user  # Access decoded JWT payload
    if request.method != 'POST':
        return JsonResponse({"error": "Use POST method"}, status=400)
    request_data = json.loads(request.body)
    task_id = request_data.get("task_id")
    description = request_data.get("description")

    updated_task = TaskUpdated.objects.create(
        task_id=task_id,
        updated_by_id=user.get("user_id"),
        update_description=description
    )

    return JsonResponse({
        "response": f"Task {task_id} updated successfully with {updated_task.update_description} having ID {updated_task.id}",
        "id": task_id,
        })

@csrf_exempt
@require_jwt
def task_retrieve_updates(request):
    user = request.jwt_user  # Access decoded JWT payload
    task_id = request.GET.get("task_id")

    updates = TaskUpdated.objects.filter(
        task_id=task_id,
        updated_by_id=user.get("user_id")
    )

    updates_list = [
        {
            "id": update.id,
            "update_description": update.update_description,
            "updated_at": update.updated_at
        }
        for update in updates
    ]

    return JsonResponse({"updates": updates_list, "total_updates": len(updates_list)})
