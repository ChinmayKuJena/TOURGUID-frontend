from django.urls import path
from .views import explore_place, explore_place_result, place_list,send_email_view
# , register,login,logout,home,user,base
from .views import Auth
urlpatterns = [
    path('register/', Auth.register, name='register'),
    path('login/', Auth.login, name='login'),
    path('logout/', Auth.logout, name='logout'),
    path('home/', Auth.home, name='home'),
    path('user/', Auth.user, name='user'),
    path('explore_place/', explore_place, name='explore_place'),
    path('explore_place_result',explore_place_result,name='explore_place_result'),
    path('places/', place_list, name='place_list'),

    path('base',Auth.base,name='base'),
    path('send-email/', send_email_view, name='send_email'),

    # path('translate/', translate_audio, name='translate_audio'),

    # path('', home, name='home'),  # Adjust as necessary
]
