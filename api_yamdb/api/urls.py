# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    register_user,
    get_user_token,
)

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

url_auth = [
    path('auth/signup/', register_user, name='signup'),
    path('auth/token/', get_user_token, name='token'),
]
urlpatterns = [
    path('v1/', include(url_auth)),
    path('v1/', include(router_v1.urls)),
]
