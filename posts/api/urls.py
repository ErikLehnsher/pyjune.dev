from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, TagViewSet, CategoryViewSet


router =routers.DefaultRouter()

router.register(r'posts', PostViewSet, basename='post')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'categories',CategoryViewSet, basename='category')
urlpatterns = [
    path('', include(router.urls)),
    
]
