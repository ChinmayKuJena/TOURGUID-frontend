from django import views
from django.urls import path
from django.contrib import admin
from .views import    blog_detail, blog_view, explore_place, explore_place_result, home, place_list,register,registration_success,login_success,login_view,logout,get_user_details,base,upload_image,image_list,delete_image,edit_blog, user_profile,view_blog

urlpatterns = [
    path('places/', place_list, name='place_list'),

    path('',base,name='home'),
    # path('',index,name='home'),
    path('register/', register, name='register'),
    path('registration-success/', registration_success, name='registration_success'),
    path('login/', login_view, name='login'),
    path('login_success/', login_success, name='login_success'),
    path('logout/', logout, name='logout'),  # Add the logout URL pattern
    path('homepage/',home,name='home'),
    path('explore_place/', explore_place, name='explore_place'),
    path('explore_place_result',explore_place_result,name='explore_place_result'),
    path('user-details/', get_user_details, name='user_details'),
    path('upload/', upload_image, name='upload_image'),
    # path('upload/', fileupload, name='upload_image'),
    path('blog_list/', image_list, name='image_list'),
    path('delete/<int:image_id>/', delete_image, name='delete_image'),    
    # path('delete-from-profile/', delete_blogimage_profile, name='delete_image'),    
    # path('delete-from-profile/<int:image_id>/', delete_image, name='delete_image'),    
    path('edit/<int:image_id>/', edit_blog, name='edit_image'),
    # path('images/<int:blog_id>/', blog_detail, name='blog_detail'),
    # path('explore_place_result/', explore_place_result, name='explore_place_result'),
    # path('view_blog/<int:blog_id>/', view_blog, name='view_blog'),
    path('profile/', user_profile, name='user_profile'),
    path('blog/<int:blog_id>/', blog_view, name='blog_view'),

]
