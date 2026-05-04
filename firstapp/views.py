from datetime import datetime, timedelta
from decouple import config
import jwt
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

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')

@csrf_exempt
def user_signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = Auth.objects.get(username=username)
        except Auth.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        try:
            ph.verify(user.password, password)
        except Exception:
            return JsonResponse({"error": "Incorrect password."}, status=400)

        # Generate JWT
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return JsonResponse({
            "message": f"User {username} signed in successfully!",
            "token": token
        })
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=400)

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(f"Received signup data: username={username}, password={password}")

        # Check if user already exists
        if Auth.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists."}, status=400)

        # Hash the password before storing it
        hashed_password = ph.hash(password)
        auth_table = Auth.objects.create(username=username, password=hashed_password)

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
