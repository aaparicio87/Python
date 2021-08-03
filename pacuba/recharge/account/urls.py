from django.urls import path
from .views import *

urlpatterns = [    
    path('forgot/',forgot, name="forgot"),
    path('register/',register, name="register"),
    path('login/',login_view, name="login"),
    path('logout/',logout_view, name="logout"),
    path('terms/',terms, name="terms"),
    path('reset/',reset, name="reset"),
    path('send_confirm/',send_confirm, name="send_confirm"),
    path('invalid_link/',invalid_link, name="invalid_link"),
    path('activate/<slug:uidb64>/<slug:token>',activate, name="activate"),
]