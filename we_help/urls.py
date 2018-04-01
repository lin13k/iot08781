from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/?$', views.EventView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='event-list'),
]
