import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/accounts/login/',  # Add your login URL here
            '/accounts/logout/',          # Add your logout URL here
            '/accounts/register/',        # Add registration URL if applicable
            '/accounts/registration-success/',
            '/home/',
        ]

    def __call__(self, request):
        if request.path in self.exempt_urls:
            return self.get_response(request)

        token = request.COOKIES.get('jwt_token')


        if not token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        print(decoded_token)
        return response
