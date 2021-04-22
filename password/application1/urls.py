from django.conf.urls import url
from application1 import views

app_name='application1'
urlpatterns = [
    url('register/',views.register,name='register'),
    url('login/',views.user_login,name='user_login'),
]
