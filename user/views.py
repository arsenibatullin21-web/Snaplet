from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from django.views.generic import CreateView, DetailView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from user.forms import UserLoginForm, UserRegisterForm
from user.models import User, Follow
from user.serializers import UserLoginSerializer, UserDetailSerializer, UserRegisterSerializer, UserUpdateSerializer, \
    ChangePasswordSerializer


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm

class UserRegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')


class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'

class OtherUserProfile(DetailView):
    model = get_user_model()
    template_name = 'user/other_profile.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_following'] = False
        profile_user = self.object
        if self.request.user.is_authenticated:
            context['if_following'] = Follow.objects.filter(
                follower=self.request.user,
                following=profile_user
            ).exists()
        return context

    def get_template_names(self):
        if self.request.user == self.object:
            return ['user/profile.html']
        return ['user/other_profile.html']

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': "You logged in successfully"
            })
        return Response(serializer.errors)


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserDetailSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': "You registered successfully"
            })
        return Response(serializer.errors)




class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return self.request.user


    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserDetailSerializer


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('new_password')
            user.set_password(password)
            user.save()
            return Response({
                'user': user.username,
                'message': "Password changed successfully"
            })
        return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    refresh = request.data.get("refresh_token")

    if not refresh:
        return Response(
            {"error": "refresh_token is required"},
            status=400
        )

    try:
        token = RefreshToken(refresh)
        token.blacklist()

        return Response({
            "message": "You logged out successfully"
        })

    except Exception:
        return Response({
            "error": "Invalid refresh token"
        }, status=400)





