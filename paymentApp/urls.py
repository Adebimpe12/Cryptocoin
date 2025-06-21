from django.urls import path, re_path
from paymentApp import views as view

urlpatterns = [  
    re_path(r'^make_payment/(?P<user_id>\d+)/', view.payNow, name="make_payment"),
    re_path(r'^payment_success/(?P<user_id>\d+)/', view.paymentSuccess, name="payment_success"),
    re_path(r'^payment_fails/(?P<user_id>\d+)/', view.paymentFail, name="payment_fails"),

]
