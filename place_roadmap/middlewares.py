from datetime import datetime
from django.shortcuts import redirect
import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            # '/home/login/',            # Add your login URL here
            # '/home/logout/',          # Add your logout URL here
            # '/home/register/',        # Add registration URL if applicable
            # '/home/registration-success/',
            # '/home/', 
            '/login/',            # Add your login URL here
            '/logout/',          # Add your logout URL here
            '/register/',        # Add registration URL if applicable
            '/registration-success/',
            '/',
        ]

    def __call__(self, request):
        if request.path in self.exempt_urls:
            return self.get_response(request)

        token = request.COOKIES.get('jwt_token')

        if not token:
            return self.redirect_to_login_with_message(request, "You are not logged in. Please log in again. .")  # Redirect to login with a message

        # if not token:
        #     return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            expiration_time = decoded_token['exp']
            if expiration_time < datetime.utcnow().timestamp():
                return self.redirect_to_login_with_message(request, "Your session has expired. Please log in again.")  # Redirect to login with a message

            request.user = decoded_token
        except jwt.ExpiredSignatureError:
            return self.redirect_to_login_with_message(request, "Your session has expired. Please log in again.")  # Redirect to login with a message
        except jwt.InvalidTokenError:
            return self.redirect_to_login_with_message(request, "Invalid token. Please log in again.")  # Redirect to login with a message


        response = self.get_response(request)
        # print(decoded_token)
        return response
    
    def redirect_to_login_with_message(self, request, message):
        # Set a message in the session
        request.session['login_message'] = message
        # Redirect to the login page
        return redirect('login')  # Replace 'login' with your actual login URL name    



