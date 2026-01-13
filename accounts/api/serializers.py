from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile






class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['avatar','avatar_url','display_name', 'bio', 'location', 'birth_date', 'website', 'github', 'twitter', 'linkedin', 'is_author', 'is_admin']
        
    def get_avatar_url(self, obj):
        if obj.avatar and hasattr(obj.avatar, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url) 
            return obj.avatar.url
        return "None"
    
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'first_name', 'last_name', 'profile', 'is_staff', 'is_active','last_login', 'date_joined']
        

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    display_name = serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email already exists')
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        display_name = validated_data['display_name']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=True
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.display_name = display_name
        profile.save()

        return user


class AdminUserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.display_name')
    role = serializers.CharField(source='profile.role')

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'date_joined',
            'display_name',
            'role',
        ]

class MeUpdateSerializer(serializers.Serializer):
    # ===== User =====
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    # ===== Profile =====
    display_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    website = serializers.URLField(required=False, allow_blank=True)
    github = serializers.URLField(required=False, allow_blank=True)
    twitter = serializers.URLField(required=False, allow_blank=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)
