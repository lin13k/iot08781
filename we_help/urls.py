from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/?$', views.NearByEventViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='nearby-event-list'),
    url(r'^events/created?$', views.CreatedEventViewSet.as_view({
        'get': 'list',
    }), name='created-event-list'),
    url(r'^events/created/(?P<pk>[0-9]+)/?$',
        views.CreatedEventViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
        }), name='created-event-detail'),
    url(r'^event/(?P<pk>[0-9]+)/?$', views.NearByEventViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update',
    }), name='event-detail'),
    url(r'^event/(?P<pk>[0-9]+)/signup/?$',
        views.SignupEventView.as_view(), name='event-signup'),
    url(r'^events/signed?$', views.SignedEventViewSet.as_view({
        'get': 'list',
    }), name='signed-event-list'),

    url(r'^events/photo/(\d+)/?$',
        views.EventPhotoView.as_view(), name='event-photo'),

]
