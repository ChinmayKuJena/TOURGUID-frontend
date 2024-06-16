# yourapp/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from .models import UserRegistration
import jwt

class FetchUserDetailsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt_token')
        if token:
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_token.get('id')
                if user_id:
                    user = UserRegistration.objects.get(id=user_id)
                    request.user_details = {
                        'username': f"{user.first_name} {user.last_name}",
                        'email': user.email,
                    }
                    request.authenticated = True
                else:
                    request.user_details = None
                    request.authenticated = False
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, UserRegistration.DoesNotExist):
                request.user_details = None
                request.authenticated = False
        else:
            request.user_details = None
            request.authenticated = False
