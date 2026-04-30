from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import TaskCreation, TaskUpdated

# Create your views here.
@csrf_exempt
def task_creation(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        return JsonResponse({"json body": request_data})

@csrf_exempt
def task_retrieval(request):
    pass