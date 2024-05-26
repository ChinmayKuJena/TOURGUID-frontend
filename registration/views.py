from django.utils import timezone
from django.shortcuts import render, redirect
import jwt
from django.conf import settings
from .models import UserRegistration
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            form.save()
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = UserRegistration.objects.get(email=email)
                if user and check_password(password, user.password):
                    print("password correct")
                    # Generate JWT token
                    payload = {
                        'id': user.id,
                        'email': user.email,
                        'exp': datetime.utcnow() + timedelta(hours=1),  # Token expiry time
                        'username':(user.first_name +" "+ user.last_name),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    
                    # Update the user token and last login
                    user.token = token
                    user.last_login = timezone.now()
                    user.save()

                    # Set the token in the cookie
                    response = redirect('login_success')
                    response.set_cookie('jwt_token', token, httponly=True, expires=payload['exp'])

                    return response
                else:
                    form.add_error(None, 'Invalid email or password')
            except UserRegistration.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def login_success(request):
    token = request.COOKIES.get('jwt_token')
    return render(request, 'login_success.html', {'token': token})

@csrf_exempt
def logout(request):
    # Clear the user's session or remove authentication tokens from cookies
    response = redirect('login')  # Redirect to the login page
    response.delete_cookie('jwt_token')  # Delete the JWT token cookie if it exists
    return response

def get_user_details(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_details = {
            'username': decoded_token['username'],  # Assuming username is stored in the JWT token
            'email': decoded_token['email'],        # Assuming email is stored in the JWT token
            # Add other user details as needed
        }
        return JsonResponse(user_details)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)