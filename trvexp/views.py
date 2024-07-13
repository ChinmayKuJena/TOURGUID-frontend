import random
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
import jwt
import requests

from .forms import RegistrationForm, LoginForm, SearchForm
from .models import UserTable
from .images import state_images
from .const import jwtDecoder,jwtDecoderName,jwtDecoder2,send_simple_email
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email_view(request):
    if request.method == 'POST':
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_simple_email(to_email, subject, message)
        # return HttpResponse("Email sent successfully!")
        render(request, 'send_email.html')
    return render(request, 'send_email.html')
def login_email(user):
    # Context to pass to the email template
    context = {
        'user': user,
    }

    # Render the email content from the template
    email_content = render_to_string('login_email.html', context)

    # Sending email
    send_mail(
        "Welcome To Travel Exploration",  # Subject
        '',  # Message (optional, content already in email_content)
        settings.EMAIL_HOST_USER,  # From email address (configured in settings)
        [user.email],  # To email addresses (can be a list of recipients)
        html_message=email_content,  # HTML content
    )
def register_email(user):
    # Context to pass to the email template
    context = {
        'user': user,
    }

    # Render the email content from the template
    email_content = render_to_string('signup_email.html', context)

    # Sending email
    send_mail(
        "Registration Complete",  # Subject
        '',  # Message (optional, content already in email_content)
        settings.EMAIL_HOST_USER,  # From email address (configured in settings)
        [user.email],  # To email addresses (can be a list of recipients)
        html_message=email_content,  # HTML content
    )
random_id = ''.join([str(random.randint(0, 9)) for _ in range(5)])
# class having all user login and register datas
class Auth():
    def home(request):
        return render(request,  'home.html')
    def base(request):
        return render(request, 'base2.html')

    def register(request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                firstName = form.cleaned_data['firstName']
                lastName = form.cleaned_data['lastName']
                password = form.cleaned_data['password']
                hashed_password = make_password(password)

                user = UserTable(
                    email=email,
                    firstName=firstName,
                    lastName=lastName,
                    password=hashed_password,
                    joinDate=timezone.now(),
                    new=True
                )
                user.save()

                # subject = 'Registration Complete'
                # message = f'Welcome to Our Platform.\nHello {firstName} {lastName}.\n\nYour UserID:{user.userId} & UserName:{user.userName}.\n\nYour registration with Travel Exploration is complete. You can now login to explore our services.\n\nThank you!'
                # from_email = 'travel.exploooration@example.com'  # Update with your email address
                # recipient_list = [email]  
                # send_mail(subject, message, from_email, recipient_list)
                user_ip = request.META.get('REMOTE_ADDR', None)
                if user_ip:
                    print(f"New registration from {user_ip}")
                register_email(user)
                return redirect('login')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    
    def login(request):
        message = request.session.pop('login_message', None)

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email_or_userId = form.cleaned_data['email_or_userId']
                password = form.cleaned_data['password']

                # Check if email_or_userId contains '@' to determine whether it's email or userId
                if '@' in email_or_userId:
                    # Authenticate using email
                    user = UserTable.objects.filter(email=email_or_userId).first()
                else:
                    # Authenticate using userId
                    user = UserTable.objects.filter(userId=email_or_userId).first()

                if user and check_password(password, user.password):
                    # Update last login date
                    user.lastloginDate = timezone.now()
                    # #####
                    user_ip = request.META.get('REMOTE_ADDR', None)
                if user_ip:
                    print(f"New registration from {user_ip}")
                    if not user.new == False:
                        login_email(user)
                    user.new = False
                    
                    # Generate JWT token
                    payload = {
                        'userId': user.userId,
                        'userName': user.userName,
                        'email': user.email,
                        'password':user.password,
                        'password2':password,
                        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
                    }
                    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    user.jwtToken = jwt_token
                    user.jwtExpTime = timezone.now() + timedelta(hours=24)
                    user.save()
    
                    # Set JWT in cookies
                    response = redirect('home')
                    response.set_cookie('jwt_token', jwt_token, httponly=True, samesite='Lax')
                    return response
                else:
                    # Authentication failed
                    message = 'Invalid credentials. Please try again.'
            else:
                # Form is invalid
                message = 'Invalid form data. Please check the fields.'

        else:
            form = LoginForm()

        return render(request, 'login.html', {'form': form, 'message': message})


    def logout(request):
        # Clear the user's session or remove authentication tokens from cookies
        response = redirect('login')  # Redirect to the login page
        token = request.COOKIES.get('jwt_token')
        if token:
            try:
                #  JWT token and extract user ID and update the expiri time and delete the jwt token from cookie
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                userId = decoded_token.get('userId')
                user = UserTable.objects.get(userId=userId)
                print(user)
                user.lastlogoutDate = timezone.now()
                user.jwtExpTime = timezone.now()  # Set token expiration to current time
                user.save()
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, UserTable.DoesNotExist):
                pass
        response.delete_cookie('jwt_token')  # Delete the JWT token cookie if it exists
        return response

    def user(request):
    
        try:
            # userDetails = UserTable.objects.get(email=user_email)
            userDetails = UserTable.objects.get(email=jwtDecoder(request))
            print(jwtDecoderName(request),"try")
        except UserTable.DoesNotExist:
            userDetails = None
        print(userDetails)
        context = {
            'userDetails': userDetails,
            # 'form': form

        }
        
        return render(request, 'account.html', context)
        # return None

def place_list(request):

    
    states = []
    places = []
    selected_state = None
    selected_place = None

    with connection.cursor() as cursor:
        # Fetch all states
        cursor.execute("SELECT id, state FROM india")
        states = cursor.fetchall()
        # print(states)
        if request.method == "POST":
            selected_state_id = request.POST.get('state')
            # print(selected_state_id)
            if selected_state_id:
                selected_state = selected_state_id
                # Fetch places for the selected state
                (cursor.execute("SELECT placeid, placename FROM place WHERE stateid = %s", [selected_state_id]))
                places = cursor.fetchall()
                # print(places) 
                selected_place_id = request.POST.get('placename')
                if selected_place_id:
                    cursor.execute("""
                        SELECT 
                            p.placeid, 
                            p.placename,
                            p.placedetails, 
                            p.stateid, 
                            i.state AS statename
                        FROM 
                            place p
                        JOIN 
                            india i 
                        ON 
                            p.stateid = i.id
                        WHERE 
                            p.placeid = %s
                    """, [selected_place_id])


                    selected_place = cursor.fetchone()
                    request.session['place_data'] = {
                        'placeid': selected_place[0],
                        'placename': selected_place[1],
                        'placedetails': selected_place[2],
                        'stateid': selected_place[3],
                        'state': selected_place[4],
                    }
                    return redirect('explore_place_result')

    return render(request, 'place_list.html', {
        'states': states,
        'places': places,
        'selected_state': selected_state,
        'selected_place': selected_place,
    })

def explore_place(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            place_name = form.cleaned_data['place_name']
            print(f"User searched for: {place_name}")
            place_name=place_name.lower()
            print(f"User searched for: {place_name}")
            api_url = f"http://localhost:3030/api/GetPlaceDetails/{place_name}"
            response = requests.get(api_url)
            if response.status_code == 200:
                # Store the data in the session
                request.session['place_data'] = response.json()
                response=redirect('explore_place_result')
                return response
                # return redirect('explore_place_result')
            else:
                return HttpResponse("Failed to fetch place details.")
    else:
        form = SearchForm()
    return render(request, 'explore_place.html', {'form': form})

def explore_place_result(request):
    data = request.session.get('place_data')

    if not data:
        return HttpResponse("No data found.")



    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    
    state_id = data.get('stateid')
    image_url = state_images.get(state_id, 'https://media.istockphoto.com/id/502811578/photo/india.jpg?s=1024x1024&w=is&k=20&c=Ls_9K3drasbw5O4MtG40wKjEmK7kE-EnppZBfxz_G2I=')
    # for specific json data
    # image = ImageBlogModel.objects.all()

    place_id = data.get('placeid')
    place_name = data.get('placename')
    # if not place_id==None:
    #     blogs = ImageBlogModel.objects.filter(place_id=place_id)
    # elif not place_name==None:
    #     blogs = ImageBlogModel.objects.filter(place_name=place_name)

    # print(blogs)
    context = {
        'state': data.get('state'),
        'place_name': data.get('placename'),
        'place_details': data.get('placedetails'),
        'image_url': image_url,
        # 'authenticated': True,
        # 'user_details': request.user_details,
        # 'blogs':blogs,

    }
    return render(request, 'explore_place_result.html', context)

