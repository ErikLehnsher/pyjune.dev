from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    MeView,
    AuthorDetailView,
    AvatarUploadView,
    MyProfileUpdateView,
)

urlpatterns = [
    # ===== AUTH =====
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ===== CURRENT USER =====
    path('me/', MeView.as_view(), name='me'),
    path('me/profile/', MyProfileUpdateView.as_view(), name='me-profile'),
    path('me/avatar/', AvatarUploadView.as_view(), name='me-avatar'),

    # ===== PUBLIC =====
    path('authors/<str:username>/', AuthorDetailView.as_view(), name='author-detail'),
]
