# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, post_login, CustomLogoutView, \
    token_refresh

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', post_login, name='custom-login'),
    path('auth/logout/', CustomLogoutView.as_view(), name='custom-logout'),
    path('auth/token/', token_refresh, name='custom-token-obtain-pair'),
]
