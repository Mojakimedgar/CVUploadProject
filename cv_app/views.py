from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, CVUploadForm
from django.contrib.auth.decorators import login_required
from .models import UserCV
import pandas as pd
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'cv_app/home.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'cv_app/register.html', {'form': form})

@csrf_protect
def user_login(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'cv_app/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required(login_url='/login/')
def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            user_cv = form.save(commit=False)
            user_cv.user = request.user
            user_cv.save()

            # Parse the Excel file using pandas
            file_path = user_cv.uploaded_file.path
            try:
                df = pd.read_excel(file_path)

                # Assuming the Excel file contains columns 'Full Name', 'Email', 'Skills'
                if 'Full Name' in df:
                    user_cv.full_name = df['Full Name'][0]
                if 'Email' in df:
                    user_cv.email = df['Email'][0]
                if 'Skills' in df:
                    user_cv.skills = df['Skills'][0]

                user_cv.save()

            except Exception as e:
                print(f"Error processing file: {e}")
                # Optionally, add an error message to be displayed to the user

            return redirect('home')
    else:
        form = CVUploadForm()
    return render(request, 'cv_app/upload_cv.html', {'form': form})