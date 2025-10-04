from django.urls import path, include
from . import views
from users import urls as usersUrls

urlpatterns = [
    path('register/user/', views.register_user, name='register_user'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    #path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    #path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),  # داشبورد یکپارچه برای هر دو کاربر و دکت
    path('edit_profile/', views.edit_profile, name='edit_profile'),    
]
