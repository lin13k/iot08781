from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from . import views

urlpatterns = [
    url(r'^api/users/?$', views.UserCreate.as_view(), name='account-create'),
    url(r'^api/login/?$', obtain_jwt_token, name='account-login'),
    url(r'^api/refresh/?$', refresh_jwt_token, name='account-refresh'),
    url(r'^api/verify/?$', verify_jwt_token, name='account-verify'),
    url(r'^api/profile/(?P<pk>[0-9]+)/?$',
        views.ProfileViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
        }), name='profile'),
]
