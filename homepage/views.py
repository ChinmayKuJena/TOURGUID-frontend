import json
from django.db import connection
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

# from .utils import COMMON_KEYS
from .forms import SearchForm,UserEditForm
import requests
from django.utils import timezone
import jwt
from django.conf import settings
from .models import UserRegistration,ImageBlogModel
from .forms import UserRegistrationForm, UserLoginForm,ImageBlogForm
from django.contrib.auth.hashers import check_password
from datetime import  timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
# from .models import Place




def image_list(request):
    blogs = ImageBlogModel.objects.all()
    return render(request, 'image_list.html', {'blogs': blogs, 'authenticated': True,'user': request.user,'user_details': request.user_details,})

def view_blog(request, blog_id):
    blog = get_object_or_404(ImageBlogModel, id=blog_id)

    context = {
        'blog': blog,
        'authenticated': True,
        'user_details': request.user_details,
        # 'image': image,
    }
    return render(request, 'view_blog.html', context)

def blog_detail(request, blog_id):
    
    # blog = get_object_or_404(ImageBlogModel, id=blog_id)
    
    blog = get_object_or_404(ImageBlogModel, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog, 'user_details': request.user_details,'authenticated': True})

# using this 
def blog_view(request, blog_id):
    blog = get_object_or_404(ImageBlogModel, id=blog_id)
    
    # Determine where to redirect based on a query parameter or POST data
    redirect_to = request.GET.get('next') or request.POST.get('next') 
    context = {
        'blog': blog,
        'authenticated': True,
        'user_details': request.user_details,
        'next': redirect_to,
    }

    return render(request, 'blog_detail.html', context)


@csrf_exempt
def delete_image(request, image_id):
    # Get the JWT token from cookies
    token = request.COOKIES.get('jwt_token')
    if not token:
        return HttpResponse("Unauthorized", status=401)
    
    try:
        # Decode the token to get the username
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        logged_in_username = decoded_token.get('username')

        # Fetch the image to be deleted
        image = get_object_or_404(ImageBlogModel, id=image_id)
        # Check if the logged-in user is the one who posted the image
        if image.username == logged_in_username:
            if request.method == 'POST':
                image.delete()
                return redirect('user_profile')
            return render(request, 'delete_image.html', {'image': image,'authenticated': True,})
        else:
            return HttpResponse("You are not authorized to delete this image.", status=403)

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return HttpResponse("Invalid or expired token", status=401)
    
   

# @login_required
def edit_blog(request, image_id):
    image = get_object_or_404(ImageBlogModel, id=image_id)
    # print(request.user.username)
    token = request.COOKIES.get('jwt_token')

    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    logged_in_username = decoded_token.get('username')
    if request.method == 'POST' and image.username == logged_in_username:
        image.blog = request.POST.get('blog')
        image.save()
        return redirect('image_list')
    return render(request, 'edit_image.html', {'image': image,'authenticated': True,'user': request.user})    



def user_profile(request):
    user_email = None
    token = request.COOKIES.get('jwt_token')
    username=None
    
    if token:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_token)
            user_email = decoded_token.get('email')
            username = decoded_token.get('username')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return redirect('login')
    # print(user_email)
    if not user_email:
        return redirect('login')
    
    try:
        userDetails = UserRegistration.objects.get(email=user_email)
    except UserRegistration.DoesNotExist:
        userDetails = None
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=userDetails)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserEditForm(instance=userDetails)    

    blogs = ImageBlogModel.objects.filter(username=username) if userDetails else ImageBlogModel.objects.none()
    # print(COMMON_KEYS['USER_DETAILS_OBJ'])
    context = {
        'userDetails': userDetails,
        'blogs': blogs,
        'authenticated': True,
        'user_details': request.user_details,
        'form': form

    }
    
    return render(request, 'account.html', context)



def upload_image(request):
    # Get place_data from session, initialize as an empty dict if not present
    place_data = request.session.get('place_data', {})
    print(place_data)
    # Check if place_data is a list and convert to a dictionary if necessary
    if isinstance(place_data, list):
        place_data = place_data[0] if place_data else {}
        username = 'anonymous'

    # Get the JWT token from cookies
    token = request.COOKIES.get('jwt_token')
    if token:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            username = decoded_token.get('username', 'anonymous')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            pass    

    context = {
        'state': place_data.get('state', ''),
        'place_name': place_data.get('placename', ''),
        'place_details': place_data.get('placedetails', ''),
        'username': username,
        
    }
    # print(context.get('user_details'))
    if request.method == 'POST':
        form = ImageBlogForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new instance without saving it to the database yet
            image_blog = form.save(commit=False)
            # Set additional fields from session data
            image_blog.state_name = place_data.get('state', '')
            image_blog.state_id = place_data.get('stateid', '')
            image_blog.place_name = place_data.get('placename', '')
            image_blog.place_id = place_data.get('placeid', '')
            # Set username from cookies
            image_blog.username = username
            

            # Save the instance to the database
            image_blog.save()
            
            return redirect('image_list')
            # return render(request, 'upload_image.html', {'form': form, 'context': context,'authenticated': True,'user_details': request.user_details})
    else:
        form = ImageBlogForm()

    return render(request, 'upload_image.html', {'form': form, 'context': context,'authenticated': True,'user_details': request.user_details,'place_data':place_data})


def place_list(request):
    username = 'anonymous'
    token = request.COOKIES.get('jwt_token')
    if token:
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = decoded_token.get('username', 'anonymous')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            pass
    
    states = []
    places = []
    selected_state = None
    selected_place = None

    with connection.cursor() as cursor:
        # Fetch all states
        cursor.execute("SELECT id, state FROM india")
        states = cursor.fetchall()
        
        if request.method == "POST":
            selected_state_id = request.POST.get('state')
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
                        'stateid': selected_place[2],
                        'state': selected_place[3],
                        # 'placedetails': selected_place[4],
                    }
                    return redirect('upload_image')

    return render(request, 'place_list.html', {
        'states': states,
        'places': places,
        'selected_state': selected_state,
        'selected_place': selected_place,
        'username': username,
        'authenticated': True,
        'user_details': request.user_details
    })

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')

@csrf_exempt
def login_view(request):
    message = request.session.pop('login_message', None)

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = UserRegistration.objects.get(email=email)
                if user and check_password(password, user.password):
                    # jwt expiry time 
                    token_expiration = timezone.now() + timedelta(minutes=100000)
                    # payload with userid user email and username
                    payload = {
                        'id': user.id,
                        'email': user.email,
                        'exp': token_expiration,
                        'username': f"{user.first_name} {user.last_name}",                        
                    }

                    # jwt token 
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    # save in db
                    user.token = token
                    user.token_expiration = token_expiration
                    user.last_login = timezone.now()
                    user.save()
                    # ############# #
                    response = redirect('login_success')
                    # jwt set to cookie
                    response.set_cookie('jwt_token', token, httponly=True, expires=payload['exp'])
                    return response
                else:
                    form.add_error(None, 'Invalid email or password')
            except UserRegistration.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form,'message':message})

def login_success(request):
    token = request.COOKIES.get('jwt_token')
    return render(request, 'login_success.html', {'token': token,'authenticated': True,'user_details': request.user_details})

@csrf_exempt
def logout(request):
    # Clear the user's session or remove authentication tokens from cookies
    response = redirect('login')  # Redirect to the login page
    token = request.COOKIES.get('jwt_token')
    if token:
        try:
            #  JWT token and extract user ID and update the expiri time and delete the jwt token from cookie
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('id')
            user = UserRegistration.objects.get(id=user_id)
            user.last_logout = timezone.now()
            user.token_expiration = timezone.now()  # Set token expiration to current time
            user.save()
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, UserRegistration.DoesNotExist):
            pass
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

def home(request):
    return render(request, 'home.html',{'authenticated': True,'user_details': request.user_details})

def base(request):
    token = request.COOKIES.get('jwt_token')

    if token:
        try:
            authenticated = True
        except jwt.ExpiredSignatureError:

            authenticated = False
        except jwt.InvalidTokenError:

            authenticated = False
    else:
        authenticated = False

    return render(request, 'base2.html', {'authenticated': authenticated, 'user_details': request.user_details})

def explore_place(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            place_name = form.cleaned_data['place_name']
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
    return render(request, 'explore_place.html', {'form': form,'authenticated': True,'user_details': request.user_details})

def explore_place_result(request):
    data = request.session.get('place_data')

    if not data:
        return HttpResponse("No data found.")



    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    state_images = {
    'OD': 'https://media.istockphoto.com/id/1544985756/photo/odisha-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=W2R-rFG7DrDlyC-qMxHZD-Aw2Iuy3Gbb0jV-UG8FcBE=',
    'JH': 'https://media.istockphoto.com/id/1544985416/photo/jharkhand-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=P3uRE8g2s8NIi2Ef_2XvLoCMdK5tVzb7g1Lc91-jzkQ=',
    'SK': 'https://media.istockphoto.com/id/1544985948/photo/sikkim-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=d8vnYpuEga6yzHnMIXxagoHAISBn7HXv7oeHyhcueO4=',
    'PB': 'https://media.istockphoto.com/id/1544985944/photo/punjab-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=qtzjO6k3ID_OPcTXlEqF_NVuP_yX4zPi2YeM7kVCSaU=',
    'ML': 'https://media.istockphoto.com/id/1544985428/photo/meghalaya-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=lalaGG90nJd68L5QstAHixLxxJ1T6VIB9__tprwCTcg=',
    'MH': 'https://media.istockphoto.com/id/1544985420/photo/maharashtra-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=q_dxGh58hvk83ZElYT37f7UfiTsL8DFKzm-drfHc2cU=',
    'NL': 'https://static.vecteezy.com/system/resources/previews/036/124/901/original/nagaland-state-map-location-in-indian-3d-isometric-map-nagaland-map-illustration-vector.jpg',
    'UK': 'https://media.istockphoto.com/id/1544985958/photo/uttarakhand-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=rp9BidW9u9Q7QD7-MKnE5sD_K8i7UiZ2i6-JblJ_9NA=',
    'MZ': 'https://media.istockphoto.com/id/1544985947/photo/mizoram-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=48cW-20CLnIEQhXBY3gJDsyrbOVYZ-cxeIgCbI_yfBc=',
    'AR': 'https://media.istockphoto.com/id/1544984896/photo/arunachal-pradesh-and-nagaland-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=Zq2E05wuAbIHXIdd4tZQmH7ZFvYteLgAIej-G83mfRU=',
    'WB': 'https://media.istockphoto.com/id/1544985962/photo/west-bengal-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=CW-5Dk40HtHN7MpafPoeqjLh6868p9-yC0e-_5-GK7A=',
    'KL': 'https://media.istockphoto.com/id/1460444658/vector/india-map-graphic-travel-geography-icon-indian-region-kerala-vector-illustration.jpg?s=1024x1024&w=is&k=20&c=TsFOeVcQXzHHTmHM_XeWGBfv4o5v5mEDMq3bnj0jr84=',
    'CG': 'https://media.istockphoto.com/id/1184114632/vector/chhattisgarh-red-highlighted-in-map-of-india.jpg?s=1024x1024&w=is&k=20&c=nYAanpBZ5eY6ma_D1GYxkwYvrbEZWv6PEV5KQ7nIIVY=',
    'KA': 'https://media.istockphoto.com/id/1544985417/photo/karnataka-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=BVUOlyXXSpwY7fSzHTJ2jteVP74xLfHicxcd_jn0-cU=',
    'GJ': 'https://media.istockphoto.com/id/1544985405/photo/gujarat-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=PPHkgt0RpaaCsyNp6q6vhDrCika3tT0S8vKsj_tvMHU=',
    'MN': 'https://media.istockphoto.com/id/1544985427/photo/manipur-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=t87SwSX5_tdLm-043N9l5LU4ZpF428f8mnUgU8kBz60=',
    'BR': 'https://media.istockphoto.com/id/850869380/vector/bihar-red-on-gray-india-map-vector.jpg?s=1024x1024&w=is&k=20&c=e8XOp0PcJw81mrQcvXXPQRci0d_eBrd6r003Nxzy8vA=',
    'UP': 'https://media.istockphoto.com/id/1544985957/photo/uttar-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=PTs-UNrzPFn7Swu0umveenbS-b7m7Kdks6lI9FDof44=',
    'HP': 'https://media.istockphoto.com/id/1544985411/photo/himachal-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=DDERq8_7ps39l8PFrKB8Gv4FwSR8ehbp6C5ewMVGG_c=',
    'AP': 'https://media.istockphoto.com/id/1544984897/photo/andhra-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=clBP8WsrpvwLdiUASL3g1MiEU6Cp-t0SHskOuqeMq6c=',
    'TN': 'https://media.istockphoto.com/id/1544985952/photo/tamil-nadu-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=UCA2p-JdeCcn_rELhwoXXvoeqvTIdJpdYC--EF6US8E=',
    'TR': 'https://media.istockphoto.com/id/1544985954/photo/tripura-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=FZEx7wcZBYv0Bce0jdogAhmbgKT6K82t9Kiy9sJ0NYY=',
    'RJ': 'https://media.istockphoto.com/id/1544985951/photo/rajasthan-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=C5eXesReNaNwh7XJ6T2f92RFFbHj6WG2omYynr6olwY=',
    'TS': 'https://media.istockphoto.com/id/1544985955/photo/telangana-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=YKeGjJVbgNPjSxjHDujCUII_NQm7XDSZA-fTC6d4K-I=',
    'MP': 'https://media.istockphoto.com/id/1544985421/photo/madhya-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=SrSOcH7up3rtYFmBg0fXjEA5Z0WMq-aNEBl2DACkoB8=',
    'HR': 'https://static.vecteezy.com/system/resources/previews/036/124/850/original/haryana-map-location-in-indian-3d-isometric-map-haryana-map-illustration-vector.jpg',
    'AS': 'https://media.istockphoto.com/id/1544984892/photo/assam-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=ITdRHu1nBsM42TnypyTfh-lVGHdi9cSOjQaay2oFrao=',
    'GA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/IN-GA.svg/450px-IN-GA.svg.png',
}

    
    state_id = data.get('stateid')
    image_url = state_images.get(state_id, 'https://media.istockphoto.com/id/502811578/photo/india.jpg?s=1024x1024&w=is&k=20&c=Ls_9K3drasbw5O4MtG40wKjEmK7kE-EnppZBfxz_G2I=')
    # for specific json data
    # image = ImageBlogModel.objects.all()

    place_id = data.get('placeid')
    place_name = data.get('placename')
    if not place_id==None:
        blogs = ImageBlogModel.objects.filter(place_id=place_id)
    elif not place_name==None:
        blogs = ImageBlogModel.objects.filter(place_name=place_name)

    # print(blogs)
    context = {
        'state': data.get('state'),
        'place_name': data.get('placename'),
        'place_details': data.get('placedetails'),
        'image_url': image_url,
        'authenticated': True,
        'user_details': request.user_details,
        'blogs':blogs,

    }
    return render(request, 'explore_place_result.html', context)

