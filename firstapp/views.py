from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from argon2 import PasswordHasher
from django.views import View
# Our Files
from .models import Auth

# Create your views here.
ph = PasswordHasher()

@csrf_exempt
def user_signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = Auth.objects.filter(username=username)  # Check if the user exists in the database
        if not user.exists():
            return JsonResponse({"error": "User not found."}, status=404)

        correct_password = ph.verify(user.first().password, password)  # Verify the password using argon2
        if not correct_password:
            return JsonResponse({"error": "Incorrect password."}, status=400)

        # Here you would typically authenticate the user
        return JsonResponse({"message": f"User {username} signed in successfully!"})
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=400)

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(f"Received signup data: username={username}, password={password}")

        # Hash the password before storing it
        hashed_password = ph.hash(password)
        auth_table = Auth.objects.create(username=username, password=hashed_password)

        # Here you would typically create a new user
        return JsonResponse({"message": f"User {auth_table.username} signed up successfully, with id {auth_table.id}!"})
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=400)



def hello_world(request):
    name = request.POST.get('name', 'World')
    return JsonResponse({"message": f"Hello, {name}!"})

class HelloWorldView(View):
    def get(self, request):
        name = request.GET.get('name', 'World')
        return HttpResponse(f"Hello, {name}! class-based view")
    
