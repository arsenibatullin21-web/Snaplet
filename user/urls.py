from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/<int:user_id> ', views.UserProfileView.as_view(), name='profile'),
    path('profile/others/<int:user_id>', views.OtherUserProfile.as_view(), name='other_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('api/v1/login/', views.UserLoginAPIView.as_view()),
    path('api/v1/register/', views.UserRegisterAPIView.as_view()),
    path('api/v1/profile/', views.UserProfileAPIView.as_view()),
    path('api/v1/change_password/', views.ChangePasswordAPIView.as_view()),
    path('api/v1/logout/', views.logout_view),
    path('api/v1/refresh/', TokenRefreshView.as_view())
]
