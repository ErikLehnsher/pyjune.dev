from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, RegisterSerializer, MeUpdateSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404  
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView



class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
class AuthorDetailView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile = request.user.profile
        avatar = request.FILES.get('avatar')

        if not avatar:
            return Response(
                {'detail': 'No avatar provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.avatar = avatar
        profile.save()

        return Response(
            {'avatar_url': profile.avatar.url},
            status=status.HTTP_200_OK
        )
        
        
class MyProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = MeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = request.user
        profile = user.profile
        data = serializer.validated_data

        # ===== UPDATE USER =====
        for field in ['email', 'first_name', 'last_name']:
            if field in data:
                setattr(user, field, data[field])
        user.save()

        # ===== UPDATE PROFILE =====
        profile_fields = [
            'display_name',
            'bio',
            'location',
            'birth_date',
            'website',
            'github',
            'twitter',
            'linkedin'
        ]
        for field in profile_fields:
            if field in data:
                setattr(profile, field, data[field])
        profile.save()

        return Response(
            UserSerializer(user, context={'request': request}).data,
            status=status.HTTP_200_OK
        )



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes =[AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # 👉 response UserSerializer
        return Response(
            UserSerializer(user, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
        
class LoginView(TokenObtainPairView):
    pass