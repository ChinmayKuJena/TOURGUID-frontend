from django.conf import settings
from django.db import connection
import jwt
from requests import request

# user_details=request.session.get('place_data')
# token = None
# with connection.cursor() as cursor:
#     cursor.execute("")

# if token:

#     decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#     user_details=decoded_token    

COMMON_KEYS = {
    'AUTHENTICATED': 'authenticated',
    # 'USER_DETAILS': user_details,
    'BLOGS': 'blogs',
    'USER_DETAILS_OBJ': 'userDetails',
}


