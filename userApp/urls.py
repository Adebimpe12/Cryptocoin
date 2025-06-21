from django.urls import path, re_path
from userApp import views as view

urlpatterns = [
    re_path(r'^my_profile/(?P<user_id>\d+)/', view.myProfile, name = "my_profile"),
    re_path(r'^edit_profile/(?P<user_id>\d+)', view.editProfile, name = "edit_profile"),
    re_path(r'^deactivate_profile/(?P<user_id>\d+)/', view.deactivateProfile, name= "deactivate_profile"),
    re_path(r'^view_staff/', view.allStaff, name = "view_staff"),
    re_path(r'^view_customers/', view.allCustomers, name = "view_customers"),
    re_path(r'^delete_user/(?P<user_id>\d+)/', view.deleteUser, name = "delete_user"),
]