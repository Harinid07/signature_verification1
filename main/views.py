from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage
import random

# Home page with login and register buttons
def home(request):
    return render(request, 'main/home.html')

# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'main/register.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload')
    return render(request, 'main/login.html')

# Upload and classify view
def upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        upload_image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(upload_image.name, upload_image)
        uploaded_file_url = fs.url(filename)  # Save and get the file URL

        # Dummy predictions for each model
        models = ['Bi-RNN', 'CRNN', 'RNN']
        predictions = []
        for model in models:
            label = "Forged" if random.random() > 0.5 else "Genuine"
            accuracy = f"{random.uniform(70, 95):.2f}%"  # Random accuracy between 70% and 95%
            predictions.append({'model': model, 'label': label, 'accuracy': accuracy})

        return render(request, 'main/upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'predictions': predictions,
        })

    return render(request, 'main/upload.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')
