from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

# Create your views here.
@csrf_exempt
def task_creation(request):
    pass

@csrf_exempt
def task_retrieval(request):
    pass