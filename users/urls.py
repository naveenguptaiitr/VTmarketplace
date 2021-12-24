from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='create_account'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profileedit/<str:username>', views.profile_edit, name='profile_edit'),
    path('editdetails/<str:username>', views.edit_detail, name='profile_edit_detail'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
]
