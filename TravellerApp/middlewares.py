from datetime import datetime
from django.shortcuts import redirect
import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/trv/register/',  # Register URL
            '/trv/login/',     # Login URL
        ]

    def __call__(self, request):
        if request.path in self.exempt_urls:
            return self.get_response(request)

        token = request.COOKIES.get('jwt_token')

        if not token:
            return self.redirect_to_login_with_message(request, "You are not logged in. Please log in again.")

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            expiration_time = decoded_token['exp']
            
            if expiration_time < datetime.utcnow().timestamp():
                return self.redirect_to_login_with_message(request, "Your session has expired. Please log in again.")
            
            request.user = decoded_token

        except jwt.ExpiredSignatureError:
            return self.redirect_to_login_with_message(request, "Your session has expired. Please log in again.")
        
        except jwt.InvalidTokenError:
            return self.redirect_to_login_with_message(request, "Invalid token. Please log in again.")

        response = self.get_response(request)
        return response

    def redirect_to_login_with_message(self, request, message):
        request.session['login_message'] = message
        return redirect('login')
