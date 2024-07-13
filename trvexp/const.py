from django.conf import settings
import jwt
userId = None
userName = None
def jwtDecoder2(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return None  # or return an empty string as per your preference

    # try:
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    userId = decoded_token.get('userId')
    userName = decoded_token.get('userName')
    dr=str(decoded_token)
    return dr
def jwtDecoder(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return None  # or return an empty string as per your preference

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = decoded_token.get('email')
        if email:
            return str(email)
        else:
            return None  # or return an empty string
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None  # or handle the error as needed, like logging or returning an empty string
def jwtDecoderName(request):
    token = request.COOKIES.get('jwt_token')
    if not token:
        return None  

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = decoded_token.get('userName')
        if email:
            return str(email)
        else:
            return None 
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None 
    
def user_info(request):
    userName = jwtDecoderName(request)
    return {
        'authenticated': bool(userName),
        'userName': userName,
    }


# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_simple_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )
